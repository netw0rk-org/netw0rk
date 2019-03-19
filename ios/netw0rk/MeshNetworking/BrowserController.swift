//
//  BrowserController.swift
//  netw0rk
//
//  Created by Carlos on 3/12/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import Foundation
import MultipeerConnectivity

class BrowserController{
    
    var browser: MCNearbyServiceBrowser!
    
    init(peer_id: MCPeerID){
        //Needs to be refactored into obj that handles both advertising and browsing
        let serv_type = "lifeline"
        self.browser = MCNearbyServiceBrowser.init(peer: peer_id, serviceType: serv_type)
    }
    
    func start(){
        self.browser.startBrowsingForPeers()
    }
    
    func stop(){
        self.browser.stopBrowsingForPeers()
    }
    
    func invite(){}
    
    
}
