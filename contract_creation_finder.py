#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 18:47:09 2022

@author: isaaclau
"""

import requests
import json
import time

def getBlockNum():
    url = "https://eth-mainnet.alchemyapi.io/v2/demo"
    
    payload = json.dumps({
    "jsonrpc":"2.0",
    "method":"eth_blockNumber",
    "params":[],
    "id":0
    })
    
    headers = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    res = (json.loads(response.text))
    return(int(res["result"],0))

def getCode(contract_address, block_num):
    url = "https://eth-mainnet.alchemyapi.io/v2/demo"
    
    payload = json.dumps({
        "jsonrpc":"2.0",
        "method":"eth_getCode",
        "params":[contract_address, block_num],
        "id":0
    })
    
    headers = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    res = (json.loads(response.text))
    return(res["result"])

def getTxReceipt(block_num):
    url = "https://eth-mainnet.alchemyapi.io/v2/demo"
    
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "alchemy_getTransactionReceipts",
        "params":[
            {
                "blockNumber": hex(block_num)
            }
        ],
        "id": 1
    })
    
    headers = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    res = (json.loads(response.text))
    return(res["result"]["receipts"])

# Returns index of x in arr if present, else -1
def binary_search(arr, low, high, contract_address):
 
    # Check base case
    if high >= low:
        
        mid = int((high + low)/2)
        #print("===") 
        print("high: ", high, "mid: ", mid, "low: ", low)
        
        if (high == low): 
            return low

        # If element is smaller than mid, then it can only
        # be present in left subarray
        
        if getCode(contract_address, hex(mid)) != "0x":
            return binary_search(arr, low, mid, contract_address)
 
        # Else the element can only be present in right subarray
        elif getCode(contract_address, hex(mid)) == "0x":
            return binary_search(arr, mid+1, high, contract_address)
 
    else:
        # Element is not present in the array
        return -1
 
def find_contract_deployer(contract_address):
    
    currNum = getBlockNum()
    arr = list(range(0, currNum))
     
    # Function call
    result_block_num = binary_search(arr, 0, len(arr)-1,contract_address)  
    
    receipts = (getTxReceipt(result_block_num))
    
    #print(len(receipts))
    
    for r in receipts:
        if ((r["contractAddress"]) == contract_address.lower()):
            return(r["from"], result_block_num)
        
print(find_contract_deployer('0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'))