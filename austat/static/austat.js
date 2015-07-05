$(document).ready(function(){
    $(".button-collapse").sideNav({
        menuWidth: 300
    });

    $(".modal-trigger").leanModal();

    $("#welcome.card-panel i").click(function(){
        $(this).closest('.card-panel').slideUp();
    });

    var austat = new Austat();
});

function Austat(){
    this.map = null;
    this.layers = [];
    this.answer = null;
    this.question_num = 1;
    this.question_max = 10;
    this.makeTopics();
    this.makeQuestion();
}

Austat.prototype.get_map = function(){
    if( !this.map ){
        this.map = new L.Map('map');
        
        // create the tile layer with correct attribution
        var osmUrll = 'http://otile2.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png'
        
        //var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
        var osm = new L.TileLayer(osmUrll, {minZoom: 0, maxZoom: 12, attribution: osmAttrib});
        
        // start the map in Central Australia
        this.map.addLayer(osm);
    }
    this.map.setView(new L.LatLng(-27.967335, 134.625094), 4);
    return this.map;
}

Austat.prototype.checkboxQuestion = function(question){
    var austat = this
    var tmpl = $('#question-template').html();
    var html = Mustache.render(tmpl, question);
    $('.question').html(html);
    var tmpl = $('#checkbox-template').html();
    var html = Mustache.render(tmpl, question);
    $('#checkboxes').html(html);

    $('#checkboxes input[type=radio]').click(function(){
        var selected = $(this).attr('id');
        austat.results(selected);
        return false;
    });
    $('#checkboxes').closest('.card').slideDown();
}

Austat.prototype.makeQuestion = function(){
    var austat = this;
    austat.answer = null;
    var topic = this.getRandomTopic();
    if(!topic){
        $('#notopic').slideDown();
        $('#enabletopic').click(function(e){
            $('#notopic').slideUp(function(){
                austat.makeQuestion();
            });
        });
        return;
    }
    $.ajax({
        url: '/query/' + topic,
        success: function(q){
            var l = austat.getRandomItem(q.locations);
            q.question = Mustache.render(q.question, l)
            var details = null;
            if (q.link) {
                details = q.link;
            }
            austat.answer = {value: l.value, name: l.name, details: details};
            if(l.geometry){
                austat.addPlacemarks(q)
            }else{
                austat.checkboxQuestion(q);
            }
        }
    });
}

Austat.prototype.getRandomItem = function(list){
    return list[Math.floor(Math.random()*list.length)];
}

Austat.prototype.getRandomTopic = function(){
    // Get a random topic.
    topics = this.getAllTopics();
    return this.getRandomItem(topics);
}

Austat.prototype.getAllTopics = function(){
    // Get a list of ids for selected topics.
    var topics = [];
    $('input[name=topic]').each(function(i, topic){
        if($(this).is(':checked')){
            topics.push($(this).attr('topic'));
        }
    });
    return topics;
}
Austat.prototype.makeTopics = function(){
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

Austat.prototype.results = function(selected){
    var austat = this;
    var correct = (austat.answer.value === selected);
    $.ajax({
        'url': '/leaderboard?success='+correct,
        'type': 'POST',
        'data': {success:correct}
    });
    $('#answer').closest('.card').slideDown();

    var tmpl = $('#answer-template').html();
    var html = Mustache.render(tmpl, {correct: correct, answer: austat.answer.name, details: austat.answer.details});
    $('#answer').html(html);
    $('#answer #next').click(function(){
        $(this).closest('.card').slideUp(function(){
            austat.question_num += 1;
            $('.progress .determinate').css('width', (austat.question_num * 10) + '%');
            if(austat.question_num < 10){
                austat.makeQuestion()
            }else{
                austat.gameFinished();
            }
        });
    });
}

Austat.prototype.gameFinished = function(){
    alert('GET REKT');
    this.question_num = 1;
}
Austat.prototype.addPlacemarks = function(question){
    var austat = this;
    var map = this.get_map();

    var tmpl = $('#question-template').html();
    var html = Mustache.render(tmpl, question);
    $('.question').html(html);
    $('#map').closest('.card').slideDown();
    austat.layers.forEach(function(layer){
        austat.map.removeLayer(layer);
    });
    austat.layers = [];
    question.locations.forEach(function(elem){
        var layer = L.geoJson(elem.geometry);
        layer.bindPopup(elem.name);
        layer.on('mouseover', function(e) {
            e.layer.openPopup();
        });
        layer.on('mouseout', function(e) {
            e.layer.closePopup();
        });
        layer.on('click', function(e) {
            austat.results(elem.value)
        });
        layer.openPopup();
        layer.addTo(map);
        austat.layers.push(layer);
        map.invalidateSize()
    });
}
