//lists for the buttons the player has clicked and the order of random buttons
let clickedButtons = [];
let buttonOrder = [];

let gameEnded = false;

let score = 0;


//function for start button to make new game
async function newGame() {
    buttonOrder = [];
    gameEnded = false;
    score = 0;

    //reset score counter
    document.getElementById("scoreCounter").innerHTML = "Score: "+score;

    //making start button unusable
    document.getElementById("startButton").onclick = null;

    //animation for resettion
    document.getElementById("redButton").style.backgroundColor = 'rgb(255, 255, 255)';
    document.getElementById("greenButton").style.backgroundColor = 'rgb(255, 255, 255)';
    document.getElementById("blueButton").style.backgroundColor = 'rgb(255, 255, 255)';

    await sleep(500);

    //resetting button colors
    document.getElementById("redButton").style.backgroundColor = 'rgb(199, 30, 30)';
    document.getElementById("greenButton").style.backgroundColor = 'rgb(30, 199, 30)';
    document.getElementById("blueButton").style.backgroundColor = 'rgb(30, 30, 199)';

    await sleep(1000);

    //making the buttons clickable again for player selection
    document.getElementById("redButton").onclick = function () { colorButtonOnClick('redButton'); };
    document.getElementById("blueButton").onclick = function () { colorButtonOnClick('blueButton'); };
    document.getElementById("greenButton").onclick = function () { colorButtonOnClick('greenButton'); };

    newRound();
}



//function for a new round
async function newRound() {
    score += 1;
    document.getElementById("scoreCounter").innerHTML = "Score: "+score;

    //resetting the clicked buttons
    clickedButtons = []

    //adding a new random button to the button order list
    buttonOrder.push(addRandomColor());

    //setting the onclick events for each button to false so the player can't choose the order they press in while the buttons are being highlighted
    document.getElementById("redButton").onclick = null;
    document.getElementById("blueButton").onclick = null;
    document.getElementById("greenButton").onclick = null;

    //for loop for every eleement in the list of random buttons
    for (const value of buttonOrder) {
        
        //highlighting red button
        if (value == "redButton") {
            await sleep(500);
            document.getElementById("redButton").style.backgroundColor = 'rgb(255, 30, 30)';
            await sleep(500);
            document.getElementById("redButton").style.backgroundColor ='rgb(199, 30, 30)';
        }

        //highlighting green button
        if (value == "greenButton") {
            await sleep(500);
            document.getElementById("greenButton").style.backgroundColor = 'rgb(30, 255, 30)';
            await sleep(500);
            document.getElementById("greenButton").style.backgroundColor = 'rgb(30, 199, 30)';
        }

        //highlighting blue button
        if (value == "blueButton") {
            await sleep(500);
            document.getElementById("blueButton").style.backgroundColor = 'rgb(30, 30, 255)';
            await sleep(500);
            document.getElementById("blueButton").style.backgroundColor = 'rgb(30, 30, 199)';
        }
    }

    //making the buttons clickable again for player selection
    document.getElementById("redButton").onclick = function () { colorButtonOnClick('redButton'); };
    document.getElementById("blueButton").onclick = function () { colorButtonOnClick('blueButton'); };
    document.getElementById("greenButton").onclick = function () { colorButtonOnClick('greenButton'); };
}



//end game function
async function endGame() {
    gameEnded = true;

    //making buttons unclickable to end game
    document.getElementById("redButton").onclick = null;
    document.getElementById("blueButton").onclick = null;
    document.getElementById("greenButton").onclick = null;

    //game lose animation
    await sleep(500);
    document.getElementById("redButton").style.backgroundColor = 'rgb(255, 0, 0)';
    document.getElementById("blueButton").style.backgroundColor = 'rgb(255, 0, 0)';
    document.getElementById("greenButton").style.backgroundColor = 'rgb(255, 0, 0)';

    document.getElementById("startButton").onclick = function () { newGame(); };
}



//function for each button click
function colorButtonOnClick(buttonID) {
    //pushing the button ID to track the color of each button pressed
    clickedButtons.push(buttonID);

    //checking to see if the random buttons and clicked buttons are equal
    for (b=0;b<clickedButtons.length;b++) {
        //ending game if not
        if (clickedButtons[b] != buttonOrder[b]) {
            endGame();
        }
        //continuing if yes
        if (b+1 === buttonOrder.length && gameEnded === false) {
            newRound();
        }
    }

}



//function to make a new random color
function addRandomColor() {
    //random number to decide random color
    let randomColorInt = Math.floor(Math.random() * (3 - 1 + 1) + 1)

    //if number is 1, random color is red
    if (randomColorInt == 1) {
        return "redButton";
    }
    //if number is 2, random color is blue
    if (randomColorInt == 2) {
        return "blueButton";
    }
    //if number is 3, random color is green
    if (randomColorInt == 3) {
        return "greenButton";
    }
}



//function for waiting a time
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
