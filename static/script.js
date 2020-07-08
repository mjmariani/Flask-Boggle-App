// jshint esversion:8

class BoggleGame{

    // make a new game with a new DOM id

    constructor(boardId, seconds=60 ){
        this.seconds = seconds; //length of the game
        this.showTimer();
        this.score = 0;
        this.words = new Set();
        this.board = $("#"+boardId);

        this.timer = setInterval(this.tick.bind(this), 1000); //timer will countdown 1 sec every 1000 ms ####need to go over how this works


        //get the .add-word class form from instance of game and on submit run the handleSubmit function
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this)); //binding this (specific instance of BoggleGame to the handleSubmit function)
        


    }

    //add word in list of words in index.html
    showWord(word){
        $(".words", this.board).append(`<li> ${word} </li>`);
    }

    //show score in html
    showScore(){
        $(".score", this.board).text(this.score);
    }    

    //show the status of the game

    showMessage(msg, cls){
        //find the .msg class on this.board add the message text, then remove class name, and a new class name "msg {class name}"
        $(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`); /**everytime it's looking for the msg class type, 
        it will look for the msg part of the class first ${".msg", this.board} and get the class with msg in front of name**/

    }
    
    /**
    handle submission of word: if unique and valid, increase score by length of word and show
    
    **/

    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = $(".word", this.board);
        let word = $word.val();

        //if there isn't a word then return
        if(!word) return;

        if(this.words.has(word)){
            this.showMessage(`Already found ${word}`, "error");
            return;

        }


        //check server for validity
        const resp = await axios.get("/check-word", {params: { word: word }});
        if(resp.data.result === "not-word"){
            this.showMessage(`${word} is not a valid English word`, "error");
        }else if(resp.data.result === "not-on-board"){
            this.showMessage(`${word} is not a word on this board`, "error");

        }else{
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`Added: ${word}`, "ok");
        }







        //$word.val("").focus();


    }


   //Updating the timer

    showTimer(){
        $(".timer", this.board).text(this.seconds);


    
    }

    //Tick: handle a second passing in game.

    async tick(){
        this.seconds -= 1;
        this.showTimer();

        if(this.seconds === 0){
            clearInterval(this.timer);
            await this.scoreGame();



        }

    }

    //end of the game. score and update message displayed

    async scoreGame(){
        $(".add-word", this.board).hide();
        const resp = await axios.post("/post-score", {score: this.score});
        if(resp.data.brokeRecord){
            this.showMessage(`New Record: ${this.score}`, "ok");
        }else{
            this.showMessage(`Final score: ${this.score}`, "ok");
        }

    }

}





