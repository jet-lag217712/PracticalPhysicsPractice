let answers = document.querySelectorAll(".answer")
let question = document.querySelector(".question_text").textContent
let nextButton = document.querySelector(".submit_button")
let answersNice = []
let prompt = ""
prompt += question
for (let i = 0; i < answers.length; i++) {
    answersNice[i] = answers[i].children[0].children[1]
}
console.log(answersNice)
answersNice[1].click()
nextButton.click()