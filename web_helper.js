Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

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

    // Iterate through each index in the out array
    for (let index of out) {
      if (index < 0 || index >= answerlist.length) {
        throw new Error(`Invalid answer index: ${index}`);
      }
      answerlist[index].click();
    }

    if (!nextButton) {
      throw new Error("Next button not found");
    }

    nextButton.click();
  },

  getQuestionImages: () => {
    let images = document.querySelector(".question_text").querySelectorAll("img")
    let imagelist = [];
    images.forEach((image) => {
      imagelist.push(image.src)
    });
    return imagelist;
  }

};