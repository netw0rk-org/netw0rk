//
//  Device.swift
//  netw0rk
//
//  Created by Carlos on 2/2/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import Foundation
import CoreBluetooth

struct Device {
    
    var peripheral : CBPeripheral
    var name : String
    var messages = Array<String>()
    
    init(peripheral: CBPeripheral, name:String) {
        self.peripheral = peripheral
        self.name = name
    }
}
