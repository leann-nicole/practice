
let restart = document.querySelector("#restartButton")
let board = document.querySelector("#gameBoard")
let columns = document.querySelectorAll(".columns")

restart.addEventListener("click", () => {location.reload()})

const rows = 6
const cols = 7

let grid = []
for (let row = 0; row < rows; row++)
    grid.push(new Array(cols).fill(0))

let player = 1

function resetSlots(){
    for (let i = 0; i < cols; i++){
        columns[i].addEventListener("click", dropCircle)
        columns[i].setAttribute("data-col", i)
        // create the slots for each column
        for (let j = 0; j < rows; j++){
            let slot = document.createElement("div")
            slot.className = columns[i].id 
            slot.style.backgroundColor = "rgb(19, 17, 17)" 
            slot.style.width = "60px"
            slot.style.height = "60px"
            slot.style.margin = "auto"
            slot.style.borderRadius = "50%"
            columns[i].appendChild(slot)
        }
    }
}

function displayWinner(player){
    let winner = document.querySelector("#winner")
    winner.style.backgroundColor = (player == 1)? "red" : "yellow"
    let result = document.querySelector("#result")
    result.style.visibility = "visible"
}

function winner(player){
    //check horizontally
    for (let r = 0; r < rows; r++){
        for (let c = 0; c <= cols-4; c++){
            if (grid[r][c] == player && grid[r][c+1] == player && grid[r][c+2] == player && grid[r][c+3] == player){
                displayWinner(player)
                return true
            }
        }
    }

    //check vertically
    for (let c = 0; c < cols; c++){
        for (let r = 0; r <= rows-4; r++){
            if (grid[r][c] == player && grid[r+1][c] == player && grid[r+2][c] == player && grid[r+3][c] == player){
                displayWinner(player)
                return true
            }
        }
    }

    // check diagonally
    // lowerhalf
    for (let n = 3; n < rows; n++){
        // leftmost moving upward towards the right
        for (let r = n, c = 0; r > rows-4; r--, c++){
            if (grid[r][c] == player && grid[r-1][c+1] == player && grid[r-2][c+2] == player && grid[r-3][c+3] == player){
                displayWinner(player)
                return true
            }
        }
        //rightmost moving upward towards the left
        for (let r = n, c = cols-1; r > rows-4; r--, c--){
            if (grid[r][c] == player && grid[r-1][c-1] == player && grid[r-2][c-2] == player && grid[r-3][c-3] == player){
                displayWinner(player)
                return true
            }
        }
    }

    // upperhalf
    for (let n = 2; n >= 0; n--){
        // leftmost moving downward towards the right
        for (let r = n, c = 0; r <= rows-4; r++, c++){
            console.log("log")
            console.log(grid[r][c], grid[r+1][c+1], grid[r+2][c+2], grid[r+3][c+3])
            if (grid[r][c] == player && grid[r+1][c+1] == player && grid[r+2][c+2] == player && grid[r+3][c+3] == player){
                displayWinner(player)
                return true
            }
        }
        // rightmost moving downward towards the left
        for (let r = n, c = cols-1; r <= rows-4; r++, c--){
            if (grid[r][c] == player && grid[r+1][c-1] == player && grid[r+2][c-2] == player && grid[r+3][c-3] == player){
                displayWinner(player)
                return true
            }
        }
    }
    return false
}

function dropCircle(){
    let slots = document.querySelectorAll("." + this.id)
    for (let i = rows-1; i >= 0; i--){
        if(slots[i].style.backgroundColor == "rgb(19, 17, 17)"){
            slots[i].style.backgroundColor = (player == 1)? "red" : "yellow"
            grid[i][this.getAttribute("data-col")] = player
            if (winner(player)){
                columns.forEach(column => {
                    column.removeEventListener("click", dropCircle)
                })
            }
            player = (player == 1)? 2:1  
            break
        }
    }
}

resetSlots()
