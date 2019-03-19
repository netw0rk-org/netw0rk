//
//  PeripheralManager.swift
//  netw0rk
//
//  Created by Carlos on 2/2/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import UIKit
import CoreBluetooth
import NotificationCenter
let cuuid = CBUUID.init(string: "73cc3cb7-0cbf-46d2-ba9a-b8ae6de9c143")
//var characteristics: [CBCharacteristic]!

class PeripheralManager: NSObject, CBPeripheralManagerDelegate{
    
    var manager: CBPeripheralManager!
    //var delegate: CBPeripheralManagerDelegate!
    var data: UserData!
    var service: CBMutableService!
    var sigs = [String]()
    var write: CBMutableCharacteristic!
    init(_ data: UserData){
        super.init()
        self.service = CBMutableService(type:cuuid, primary: true)
        self.service.characteristics = setCharacteristics()
        self.manager = CBPeripheralManager(delegate: self , queue: nil)
        self.data = data
    }
    
    func start(){
        if (self.manager.isAdvertising) {
            self.manager.stopAdvertising()
        }else{
            let advertisementData = String(format: "%@",data.name)
            self.manager.startAdvertising([CBAdvertisementDataServiceUUIDsKey:[data.serviceID], CBAdvertisementDataLocalNameKey: advertisementData])
            self.manager.removeAllServices()
            self.manager.add(self.service)
             NotificationCenter.default.post(name: NSNotification.Name("updatestatus"), object: nil)
        }
    }
    
    func setCharacteristics() -> [CBMutableCharacteristic]{
        let setSignature = CBMutableCharacteristic(type: CBUUID(string: "2de200df-7fe6-49e3-a768-5ff79e767fa6"),properties: [.write],value: nil,permissions: [.writeable])
        let tmp = self.data==nil ? "private_key" : self.data.privateKey
        let readPublicKey =  CBMutableCharacteristic(type: CBUUID(string: "81353fc9-33e0-4c51-994b-b52235b4d585"),properties: [CBCharacteristicProperties.read],value: tmp!.data(using: .utf8),permissions: [CBAttributePermissions.readable])
        self.write = setSignature
        return [setSignature,readPublicKey]
    }
    
    func stop(){
        self.manager.stopAdvertising()
        NotificationCenter.default.post(name: NSNotification.Name("updatestatus"), object: nil)
    }
    
    func peripheralManagerDidUpdateState(_ peripheral: CBPeripheralManager) {
        if (peripheral.state == .poweredOn){
            self.start()
        }
    }
    
    func peripheralManager(_ peripheral: CBPeripheralManager, didReceiveWrite requests: [CBATTRequest]){
        for req in requests{
            if let value = req.value {
                let sig = value
                let str_sig = String(decoding: sig, as: UTF8.self)
                self.sigs.append(str_sig)
                //self.manager.respond(to: req, withResult: .success)
            }
            self.manager.respond(to: req, withResult: .success)
        }
        NotificationCenter.default.post(name: NSNotification.Name("viewLoaded"), object: nil)
    }
    
    func peripheralManagerDidStartAdvertising(_ peripheral: CBPeripheralManager,error: Error?){
        NotificationCenter.default.post(name: NSNotification.Name("updatestatus"), object: nil)
    }
}


