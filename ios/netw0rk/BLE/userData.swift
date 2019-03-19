//
//  userData.swift
//  netw0rk
//
//  Created by Carlos on 2/2/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import Foundation
import CoreBluetooth
struct UserData {
    
    var name: String = ""
    var privateKey: String!
    var serviceID = CBUUID(string: "4DF91029-B356-463E-9F48-BAB077BF3EF5")

    var hasAllDataFilled: Bool {
        return !name.isEmpty
    }

    public init(_ name: String,_ private_key: String){
        self.name = name
        self.privateKey = private_key
    }
    
}
