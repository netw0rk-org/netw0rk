//
//  AdHocViewController.swift
//  netw0rk
//
//  Created by Carlos on 3/13/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import UIKit
import NetworkExtension

class AdHocViewController: UIViewController,UITextFieldDelegate{
    //MARK: Variables
    @IBOutlet weak var status: UILabel!
    @IBOutlet weak var onOffSwitch: UISwitch!
    
    override func viewDidLoad() {
        onOffSwitch.setOn(false,animated: false)
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
    }
    
    //MARK: SwitchControll
    @IBAction func switched(_ sender: Any) {
        if onOffSwitch.isOn {
            //start
            self.status.text = "ON"
            
        }else{
            //stop
            self.status.text = "OFF"
        }
    }
}
