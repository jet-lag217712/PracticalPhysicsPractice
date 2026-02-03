window.quizHelpers = {
  getAnswers: () => {
    let answers = document.querySelectorAll(".answer");
    let answerlist = [];

    for (let i = 0; i < answers.length; i++) {
      let el = answers[i].children[0]?.children[1];
      if (el) answerlist.push(el.textContent.trim());
    }

    return answerlist;
  },

  clickAnswerAndNext: (out) => {
    let answers = document.querySelectorAll(".answer");
    let nextButton = document.querySelector(".submit_button.next-question");
    let answerlist = [];

    for (let i = 0; i < answers.length; i++) {
      let el = answers[i].children[0]?.children[1];
      if (el) answerlist.push(el);
    }

    if (out < 0 || out >= answerlist.length) {
      throw new Error(`Invalid answer index: ${out}`);
    }

    answerlist[out].click();

    if (!nextButton) {
      throw new Error("Next button not found");
    }

    nextButton.click();
  }
};