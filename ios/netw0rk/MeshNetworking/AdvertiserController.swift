//
//  AdvertiserController.swift
//  netw0rk
//
//  Created by Carlos on 3/11/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import Foundation
import MultipeerConnectivity

class AdvertiserController {
    var advertiser: MCNearbyServiceAdvertiser!
    
    init(peer_id: MCPeerID) {
        let disc_info = ["name": "netw0rk"]
        let serv_type = "lifeline"
        self.advertiser = MCNearbyServiceAdvertiser.init(peer: peer_id, discoveryInfo: disc_info, serviceType: serv_type)
    }
    
    func start(){
        self.advertiser.startAdvertisingPeer()
    }
    
    func stop(){
        self.advertiser.stopAdvertisingPeer()
    }
}

//Storing PeerID to localDB
/**
 NSString *displayName = <#Get a name#>;
 
 NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
 NSString *oldDisplayName = [defaults stringForKey:kDisplayNameKey];
 MCPeerID *peerID;
 
 if ([oldDisplayName isEqualToString:displayName]) {
 NSData *peerIDData = [defaults dataForKey:kPeerIDKey];
 peerID = [NSKeyedUnarchiver unarchiveObjectWithData:peerIDData];
 } else {
 peerID = [[MCPeerID alloc] initWithDisplayName:displayName];
 NSData *peerIDData = [NSKeyedArchiver archivedDataWithRootObject:peerID];
 [defaults setObject:peerIDData forKey:kPeerIDKey];
 [defaults setObject:displayName forKey:kDisplayNameKey];
 [defaults synchronize];
 }

 **/
