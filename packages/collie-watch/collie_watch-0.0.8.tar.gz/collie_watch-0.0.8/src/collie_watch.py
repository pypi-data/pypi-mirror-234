
import datetime
import logging
import random
from traceback import format_exception, format_tb
from typing import List,Callable
import requests
import hashlib
import sys
import asyncio
from dataclasses import dataclass
from threading import Lock, Thread,Event
from PIL import Image
import numpy as np
from queue import SimpleQueue
import io
from contextlib import contextmanager
import time
from hashlib import sha256
from secrets import token_hex
from collections import deque
import atexit
import uuid
from supabase import create_client,Client
import websockets.client as websockets 
import json
import time
from datetime import timedelta
import psutil
import secrets

class CollieWatchEvent:
    UPDATE = "update"
    ADD_BLOCK = "add_block"
    REMOVE_BLOCK = "remove_block"
    UPDATE_BLOCK = "update_block"
    BUTTON_PRESSED = "button_pressed"


class CollieWatchButton:
    def __init__(self,button_text,callback_func) -> None:
        self.__button_text = button_text
        self.__callback_func = callback_func



class CollieWatch:
    __text_received_callback = lambda x: x
    __api_request_callback = lambda x: x
    __callbacks_map = {}
    __supabase: Client = None
    __token: str = None
    __pool: SimpleQueue = SimpleQueue()
    __thread_lock = Lock()
    __background_thread: Thread()
    __current_dashboard: dict = {}
    __dev = False
    __callbacks_to_call_sync = SimpleQueue()
    __start_time = time.monotonic()
    __program_id = None
    __program_name = None

    @staticmethod
    def has_initialized():
        return CollieWatch.__token != None

    @staticmethod
    def set_development_mode():
        CollieWatch.__dev = True
    
    @staticmethod
    def create_block(block_name):
        if "blocks" not in CollieWatch.__current_dashboard:
            CollieWatch.__current_dashboard["blocks"] = {}
        CollieWatch.__current_dashboard["blocks"][block_name] = {}
        CollieWatch.__add_to_pool(CollieWatchEvent.ADD_BLOCK,block_name)

    @staticmethod
    def set_receive_api_request_callback(callback):
        CollieWatch.__api_request_callback = callback

    

    @staticmethod
    async def ___background_thread_handler():
        print(f"starting background thread with token {CollieWatch.__token}")
        async with websockets.connect("wss://seal-app-isidc.ondigitalocean.app/" if not CollieWatch.__dev else "ws://localhost:8080",timeout=120,subprotocols=["_".join(["program",CollieWatch.__token,CollieWatch.__program_id] + ([] if CollieWatch.__program_name == None else [CollieWatch.__program_name]))]) as websocket:
            
            await asyncio.sleep(3)
            asyncio.create_task(CollieWatch.__check_for_message(websocket))
            
            while True:       
                await websocket.send(json.dumps({"type":CollieWatchEvent.UPDATE,"data":{"time":time.monotonic() - CollieWatch.__start_time,"program_id":CollieWatch.__program_id,
                      "process_data":{"cpu":psutil.cpu_percent(),"memory_used":psutil.virtual_memory().used,"memory_total":psutil.virtual_memory().total,"disk_used":psutil.disk_usage('/').used,"disk_total":psutil.disk_usage("/").total}}}))
                while not CollieWatch.__pool.empty():
                    data = CollieWatch.__pool.get()
                    await websocket.send(data)
                await asyncio.sleep(0.3)
    @staticmethod
    def __add_to_pool(event_type: str,data: dict):
        CollieWatch.__pool.put(json.dumps({"type":event_type,"data":data,"program_id":CollieWatch.__program_id}))
        
    @staticmethod
    async def __check_for_message(websocket: websockets.WebSocketClientProtocol):
        print("starting checking for messages")
        while True:
            try:
                message = await websocket.recv()
                message = json.loads(message)
                if message["type"] == CollieWatchEvent.BUTTON_PRESSED:
                    print(f'got message {message["data"]}')
                    if message["data"] in CollieWatch.__callbacks_map:
                       CollieWatch.__callbacks_to_call_sync.put(CollieWatch.__callbacks_map[message["data"]])
            
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(e)

    @staticmethod
    def run_events_sync():
        while not CollieWatch.__callbacks_to_call_sync.empty():
                callback = CollieWatch.__callbacks_to_call_sync.get()
                callback()

    @staticmethod
    def initialize(token,program_name=None):
        CollieWatch.__supabase = create_client("https://acyzjlibhoowdqjrdmwu.supabase.co","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFjeXpqbGliaG9vd2RxanJkbXd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTMyNTI2MDgsImV4cCI6MjAwODgyODYwOH0.cSP7MaxuIZUknfp-_9srZyiOmQwokEdDXlyo4mci_S8")
        try:
            data,count = CollieWatch.__supabase.from_("dashboards").select("*").eq("dashboard_token",token).execute()
            user_found = len(data[1]) != 0
            if not user_found:
                print(f'Could not find any dashboards with token "{token}".\nPlease provide a valid dashboard token!')
                return False
            CollieWatch.__program_name = program_name
            CollieWatch.__program_id = secrets.token_hex(16)
            CollieWatch.__token = token
            CollieWatch.__background_thread = Thread(target=asyncio.run,args=(CollieWatch.___background_thread_handler(),),daemon=True)
            CollieWatch.__background_thread.start()

        

            return user_found
        except Exception as e:
            print(e)
            return False
        
    
    
    
    
    @staticmethod
    def __check_if_block_exists(block_id):
        if "blocks" not in CollieWatch.__current_dashboard:
            return False
        if block_id not in CollieWatch.__current_dashboard["blocks"]:
            return False
        return True

    

    @staticmethod
    def set_text_on_block(block_id: str,message: str):
        if not CollieWatch.has_initialized():
            print("Please make sure to initialize CollieWatch before calling any of the send methods!")
            return False
        if not CollieWatch.__check_if_block_exists(block_id):
            print(f'Block with id "{block_id}" does not exist!')
            return False
        with CollieWatch.__thread_lock:
            CollieWatch.__current_dashboard["blocks"][block_id]["type"] = "text"
            CollieWatch.__current_dashboard["blocks"][block_id]["data"] = message
            CollieWatch.__add_to_pool(CollieWatchEvent.UPDATE_BLOCK,{"block_name":block_id,"block_data":CollieWatch.__current_dashboard["blocks"][block_id]})  
            

    @staticmethod
    def set_button_on_block(block_id: str,button_text: str,callback_func: Callable):
        if not CollieWatch.has_initialized():
            print("Please make sure to initialize CollieWatch before calling any of the send methods!")
            return False
        if not CollieWatch.__check_if_block_exists(block_id):
            print(f'Block with id "{block_id}" does not exist!')
            return False
        with CollieWatch.__thread_lock:
            callback_id = f"{block_id} {secrets.token_hex(10)}"
            if block_id not in CollieWatch.__callbacks_map:
                CollieWatch.__callbacks_map[block_id] = {}
            CollieWatch.__callbacks_map[block_id] = callback_func 

            CollieWatch.__current_dashboard["blocks"][block_id]["type"] = "button"
            CollieWatch.__current_dashboard["blocks"][block_id]["data"] = {
                "button_text":button_text,
                "callback_id":block_id
            }
            CollieWatch.__add_to_pool(CollieWatchEvent.UPDATE_BLOCK,{"block_name":block_id,"block_data":CollieWatch.__current_dashboard["blocks"][block_id]})  
    

    @staticmethod
    def delete_block(block_id: str):
        if not CollieWatch.has_initialized():
            print("Please make sure to initialize CollieWatch before calling any of the send methods!")
            return False
        if not CollieWatch.__check_if_block_exists(block_id):
            print(f'Block with id "{block_id}" does not exist!')
            return False
        with CollieWatch.__thread_lock:
            del CollieWatch.__current_dashboard["blocks"][block_id]
            CollieWatch.__add_to_pool(CollieWatchEvent.REMOVE_BLOCK,block_id)
        

    
    




    