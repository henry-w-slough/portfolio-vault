

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

























    
    
    
    
