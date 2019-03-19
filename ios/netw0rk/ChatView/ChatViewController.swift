//
//  ChatViewController.swift
//  netw0rk
//
//  Created by Carlos on 3/14/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import UIKit
import NotificationCenter

class ChatViewController: UIViewController,UITextFieldDelegate,UITableViewDataSource,UITableViewDelegate{
    
    //MARK: Class Variables
    //var cells = [Message]()
    var cells = [Message]()
    @IBOutlet weak var table: UITableView!
    @IBOutlet weak var inputBox: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        for i in 1...1000{
            if i % 2 == 0{
                self.cells.insert(MeMessage(msg: String(i)), at: 0)
            }else{
                  self.cells.insert(PeerMessage(msg: String(i)), at: 0)
            }
        }
        
        //self.cells = [ MeMessage(msg: "HELLO"), PeerMessage(msg: "hefsfsdfsdfsdflo\nsdfsdfsd\ns"),  ]
    
        self.inputBox.delegate = self
        
        self.table.delegate = self
        self.table.dataSource = self
        
        self.table.estimatedRowHeight = 100
        self.table.rowHeight = UITableView.automaticDimension
        
        NotificationCenter.default.addObserver(self, selector: #selector(keyboardWillShow), name:UIResponder.keyboardWillShowNotification, object: nil);
        NotificationCenter.default.addObserver(self, selector: #selector(keyboardWillHide), name:UIResponder.keyboardWillHideNotification, object: nil);
        self.table.scrollToRow(at: NSIndexPath(row: self.cells.count-1, section: 0) as IndexPath, at: .top, animated: false)
    }
    
    override func viewWillAppear(_ animated: Bool) {
      
    }
    
    //MARK: Table Protocol Methods
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.cells.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        //Grab a cell and use 
        let message = self.cells[indexPath.row]
        switch message{
            case is MeMessage:
                guard let cell = tableView.dequeueReusableCell(withIdentifier: "MeCell", for: indexPath) as? MeCell  else {
                    fatalError("The dequeued cell is not an instance of MeCell.")}
                // Configure the cell...
                cell.Message.text = message.Message
                return cell
            case is PeerMessage:
                guard let cell = tableView.dequeueReusableCell(withIdentifier: "PeerCell", for: indexPath) as? PeerCell  else {
                    fatalError("The dequeued cell is not an instance of PeerCell.")}
                // Configure the cell...
                cell.Message.text = message.Message
                return cell
            default:
                fatalError("ERROR Finding Cell Type")
        }
    }
    
    @objc private func keyboardWillShow(notification: NSNotification){
        self.view.frame.origin.y -= 200
    }
    @objc private func keyboardWillHide(){
        self.view.frame.origin.y += 200
    }
    //Clear keyboards when clicking screen
    @IBAction func tapControl(_ sender: UITapGestureRecognizer) {
        inputBox.resignFirstResponder()
    }
    //Clear keyboard when pressing done
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    //Get input from input boxes and handle appropriatley
    func textFieldDidEndEditing(_ textField: UITextField) {
        //send new message and append to my own messages
    }
}
