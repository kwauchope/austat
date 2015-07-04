var question = {
    question: 'How lame is Ben',
    answers: [
        {id: 1, answer: 'Not Really'},
        {id: 2, answer: 'A Bit'},
        {id: 3, answer: 'Heaps'},
        {id: 4, answer: 'Lamest Person Ever'},
        {id: 5, answer: 'Doesnt Know What JSON Is?'}
    ]
}

var answer = {
    answer: {
        correct: false,
        id: 5,
        details: 'Some details about the answer.'
    }
}
$(document).ready(function(){
    var tmpl = $('#question-template').html();
    var html = Mustache.render(tmpl, question);
    $('#question').html(html);
    $("#question #answer_1").prop("checked", true);

    $('#question form').submit(function(){
        var selected = $(this).find('input[name=answers]:checked').attr('id');
        results(selected);
        return false;
    });
});
function results(selected){
    if ('answer_' + answer.answer.id === selected){
        answer.answer.correct = true;
    }
    var tmpl = $('#answer-template').html();
    var html = Mustache.render(tmpl, answer);
    $('#answer').html(html);
    $('#answer #next').click(function(){
        window.location.reload();
    });
}
