//
//  SignatureTableViewCell.swift
//  netw0rk
//
//  Created by Carlos on 2/1/19.
//  Copyright © 2019 Carlos. All rights reserved.
//

import UIKit

class SignatureTableViewCell: UITableViewCell {
    //MARK: Properties
    
    @IBOutlet weak var signature: UILabel!
    @IBOutlet weak var piName: UILabel!
    
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
