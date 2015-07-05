$(document).ready(function(){
    $(".button-collapse").sideNav({
        menuWidth: 300
    });
    var austat = new Austat();

});
function Austat(){
    this.map = null;
    this.layer = null;
    this.answer = null;
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
        this.map.setView(new L.LatLng(-24.967335, 134.625094),4);
        this.map.addLayer(osm);
    }
    return this.map;
}

Austat.prototype.checkboxQuestion = function(question){
    var austat = this
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
Austat.prototype.mapSetup = function(question){
    $('#map').closest('.card').slideDown();
    this.addPlacemarks(question);
}
Austat.prototype.makeQuestion = function(){
    var austat = this;
    austat.answer = null;
    var topic = this.getRandomTopic();
    $.ajax({
        url: '/query/' + topic,
        success: function(q){
            console.log(!q['value'])
                var l = austat.getRandomItem(q.locations);
                q.question = Mustache.render(q.question, l)
                austat.answer = l.value;
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
    $('.question').closest('.card').slideUp(function(){
        $('#answer').closest('.card').slideDown();
    });
    var correct = false;
    console.log(austat.answer);
    console.log(selected);
    if (austat.answer === selected){
        correct = true;
    }
    var tmpl = $('#answer-template').html();
    var html = Mustache.render(tmpl, {correct: correct, details: 'Some Details'});
    $('#answer').html(html);
    $('#answer #next').click(function(){
        $(this).closest('.card').slideUp(function(){
            austat.makeQuestion()
            //$('#question').closest('.card').slideDown();
        });
    });
}

Austat.prototype.addPlacemarks = function(question){
    var austat = this;
    var map = this.get_map();
    var tmpl = $('#question-template').html();
    var html = Mustache.render(tmpl, question);
    $('#mapQuestion').html(html);
    $('#map').closest('.card').slideDown();
    if (this.layer){
        this.map.removeLayer(this.layer);
    }
    question.locations.forEach(function(elem){
        geom = L.geoJson(elem.geometry);
        geom.bindPopup(elem.name);
        geom.on('mouseover', function(e) {
            e.layer.openPopup();
        });
        geom.on('mouseout', function(e) {
            e.layer.closePopup();
        });
        geom.on('click', function(e) {
            austat.results(elem.value)
        });
        geom.openPopup();
        geom.addTo(map);
        this.layer = geom;
        map.invalidateSize()
    });
}
