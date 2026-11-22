var current = 0;
var score = 0;

function showQuestion(){

var q = questions[current];

document.getElementById("qNo").textContent =
"問 " + (current + 1);

document.getElementById("question").textContent =
q.q;

document.getElementById("result").innerHTML = "";

document.getElementById("explanation").innerHTML = "";

document.getElementById("nextBtn").style.display =
"none";

var choices =
document.getElementById("choices");

choices.innerHTML = "";

for(var i=0;i<q.choices.length;i++){

var btn = document.createElement("button");

btn.className = "choice";

btn.textContent = q.choices[i];

btn.setAttribute("data-index",i);

btn.onclick = function(){

checkAnswer(
parseInt(this.getAttribute("data-index"))
);

};

choices.appendChild(btn);
}

document.getElementById("totalCount")
.textContent = questions.length;

}

function checkAnswer(index){

var q = questions[current];

var buttons =
document.querySelectorAll(".choice");

for(var i=0;i<buttons.length;i++){

buttons[i].disabled = true;

}

buttons[q.answer]
.classList.add("correct");

if(index === q.answer){

score++;

document.getElementById("score")
.textContent = score;

document.getElementById("result")
.textContent = "⭕ 正解";

}else{

buttons[index]
.classList.add("wrong");

document.getElementById("result")
.textContent = "❌ 不正解";

}

document.getElementById("explanation")
.innerHTML =
"<b>解説</b><br><br>" + q.exp;

document.getElementById("nextBtn")
.style.display = "block";

}

function nextQuestion(){

current++;

if(current >= questions.length){

document.querySelector(".card").innerHTML =
"<h2>終了</h2>" +
"<p>正解数 : " +
score +
" / " +
questions.length +
"</p>";

return;
}

showQuestion();

}

document
.getElementById("nextBtn")
.addEventListener("click",nextQuestion);

showQuestion();
