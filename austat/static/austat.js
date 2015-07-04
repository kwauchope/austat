var answer = {
    answer: {
        id: 5,
        details: "Alcatra prosciutto tongue beef ribs pork loin, shoulder bresaola drumstick jowl flank venison swine kevin. Jowl pancetta turkey, pastrami ball tip hamburger spare ribs leberkas capicola tri-tip sausage. Tongue turducken jerky turkey pastrami chicken frankfurter pork chop hamburger shankle ham alcatra venison short ribs bresaola. Tri-tip filet mignon sirloin, picanha shoulder shankle porchetta ribeye kielbasa tail spare ribs swine leberkas fatback brisket. Pork loin picanha rump tongue short ribs sausage brisket beef ribs fatback, leberkas pig. Short loin alcatra bresaola venison short ribs. Beef ribs boudin meatloaf sausage pancetta corned beef. Cow tongue beef ribs venison. Shank spare ribs leberkas jowl capicola. Landjaeger frankfurter kielbasa sausage rump strip steak turkey meatloaf ribeye. Boudin turducken drumstick pork chop capicola cupim shank leberkas. Filet mignon ribeye ground round bresaola pork chop flank cupim tenderloin turducken meatloaf. Drumstick leberkas frankfurter ground round short loin. Ball tip jerky ribeye chicken kielbasa beef. Boudin sirloin ribeye ham frankfurter, doner tenderloin shoulder drumstick. Landjaeger meatball ribeye cow sausage bacon andouille. Sausage tenderloin pastrami beef ribs drumstick ribeye flank shankle tri-tip capicola meatball beef pork chop turkey picanha. Kielbasa jowl spare ribs turducken chuck shankle frankfurter ground round short ribs venison strip steak capicola picanha bacon. Jowl salami shoulder picanha doner shankle, short ribs hamburger venison biltong shank meatloaf cupim chuck. Venison frankfurter beef picanha. Turducken bacon doner ham shankle landjaeger pancetta short ribs beef ribs jowl fatback. Drumstick brisket meatloaf swine biltong shank tri-tip pig. Meatloaf chicken bresaola strip steak. Leberkas tongue boudin sausage, ball tip turkey venison shank cow. Brisket chicken shank tri-tip, short ribs frankfurter swine biltong t-bone. Frankfurter tail landjaeger prosciutto. Leberkas shankle short loin shank sirloin swine hamburger, fatback brisket tri-tip. Ribeye alcatra venison, frankfurter pastrami sirloin beef ribs tenderloin porchetta short loin. Corned beef ground round filet mignon meatloaf biltong turducken frankfurter kevin venison short ribs."
    }
}

var map = null;
function get_map(){
    if( !map ){
        map = new L.Map('map');
        // create the tile layer with correct attribution
        var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
        var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 12, attribution: osmAttrib});
        // start the map in Central Australia
        map.setView(new L.LatLng(-25.518615, 134.264176),3);
        map.addLayer(osm);
    }
    return map;
}
$(document).ready(function(){
    $(".button-collapse").sideNav({
        menuWidth: 300
    });
    makeTopics();
    makeQuestion();

});

function checkboxQuestion(question){
    var tmpl = $('#checkbox-template').html();
    var html = Mustache.render(tmpl, question);
    $('#question').html(html);

    $('#question input[type=radio]').click(function(){
        var selected = $(this).attr('id');
        results(selected);
        return false;
    });
    $('#question').closest('.card').slideDown();
}
function mapSetup(question){
    $('#map').closest('.card').slideDown();
    addPlacemarks(question);
}
function fixQuestion(q){
    console.log(q);
    return q.replace(/{/g, '{{').replace(/}/g, '}}');
}
function makeQuestion(){
    var topic = getRandomTopic();
    $.ajax({
        url: '/query/' + topic,
        success: function(q){
            q.question = fixQuestion(q.question);
            q.question = Mustache.render(q.question, getRandomItem(q.locations))
            checkboxQuestion(q);
            //var template = $('#topics-template').html();
            //var html = Mustache.render(template, topics);
            //$('#topics').html(html)
        }
    });
    //var question = questions[Math.floor(Math.random()*questions.length)];
    //if(question.type === 'CHECKBOX'){
    //    checkboxSetup(question);
    //}
    //else if (question.type === 'MAP'){
    //    mapSetup(question);
    //}
}

function getRandomItem(list){
    return list[Math.floor(Math.random()*list.length)];
}

function getRandomTopic(){
    // Get a random topic.
    topics = getAllTopics();
    return topics[Math.floor(Math.random()*topics.length)];
}

function getAllTopics(){
    // Get a list of ids for selected topics.
    var topics = [];
    $('input[name=topic]').each(function(i, topic){
        if($(this).is(':checked')){
            topics.push($(this).attr('topic'));
        }
    });
    return topics;
}

function makeTopics(){
    // Get topics from api and create controls.
    $.ajax({
        async: false,
        url: '/topics',
        success: function(topics){
            var template = $('#topics-template').html();
            var html = Mustache.render(template, topics);
            $('#topics').html(html)
        }
    });
}

function results(selected){
    $('#question').closest('.card').slideUp(function(){
        $('#answer').closest('.card').slideDown();
    });
    answer.answer.correct = false;
    if ('answer_' + answer.answer.id === selected){
        answer.answer.correct = true;
    }
    var tmpl = $('#answer-template').html();
    var html = Mustache.render(tmpl, answer);
    $('#answer').html(html);
    $('#answer #next').click(function(){
        makeQuestion()
        $(this).closest('.card').slideUp(function(){
            $('#question').closest('.card').slideDown();
        });
    });
}

function addPlacemarks(question){
    map = get_map();
    //Prototype
    question.answers.forEach(function(elem){
        geom = L.geoJson(elem['geom']);
        geom.on('click',function(evt){
            //TODO next question
        })
        canberra.addTo(map);
        
    });

}
