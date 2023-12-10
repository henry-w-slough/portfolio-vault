

all_cards_list = ["king", "king", "queen", "queen", "jack", "jack", "ace", "ace"];

toggled_cards = [];
toggled_cards_ids = [];
matchedPairs = 0


function shuffleCards() {
    var j, x, i;
    
    for (i = 8 - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = all_cards_list[i];
        all_cards_list[i] = all_cards_list[j];
        all_cards_list[j] = x;
    }

	
	console.log(all_cards_list);
}



function onCardClick(cardID) {
	cardValue = all_cards_list[cardID.substr(4)];
	toggled_cards.push(cardValue)
	toggled_cards_ids.push(cardID)
	
	print(cardValue)
	
	
	if (cardValue === "king") {
		document.getElementById(cardID).innerHTML = '<img style="width:140px;height:190px" src="https://t4.ftcdn.net/jpg/00/53/65/65/360_F_53656507_6aRlz7GvglpFMAbtf1zSsllWlepJfeTb.jpg">'
	}
	
	
	if (cardValue === "queen") {
		document.getElementById(cardID).innerHTML = '<img style="width:140px;height:190px" src="https://cdn11.bigcommerce.com/s-nq6l4syi/images/stencil/1280x1280/products/143586/524386/190996-1024__12779.1664331215.jpg?c=2?imbypass=on">'
	}
	
	
	if (cardValue === "jack") {
		document.getElementById(cardID).innerHTML = '<img style="width:140px;height:190px" src="https://i.ebayimg.com/images/g/-ScAAOSwIJViarKx/s-l1200.webp">'
	}
	
	
	if (cardValue === "ace") {
		document.getElementById(cardID).innerHTML = '<img style="width:140px;height:190px" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Ace_of_spades.svg/800px-Ace_of_spades.svg.png">'
	}
		
	
	if (toggled_cards.length === 2) {
	
		if (toggled_cards[0] === toggled_cards[1]) {
			
			document.getElementById(toggled_cards_ids[0]).removeAttribute("onclick");
			document.getElementById(toggled_cards_ids[1]).removeAttribute("onclick");
			
			toggled_cards = []
			toggled_cards_ids = []
			matchedPairs += 1
			
		}
}

}





















    
    
    
    
