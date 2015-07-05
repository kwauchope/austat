$(document).ready(function(){
    $(".button-collapse").sideNav({
        menuWidth: 300
    });
    var austat = new Austat();

});
function Austat(){
    this.map = null;
    this.layer = null;
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
    var tmpl = $('#checkbox-template').html();
    var html = Mustache.render(tmpl, question);
    $('#question').html(html);
    var mapObj = this
    $('#question input[type=radio]').click(function(){
        var selected = $(this).attr('id');
        mapObj.results(selected);
        return false;
    });
    $('#question').closest('.card').slideDown();
}
Austat.prototype.mapSetup = function(question){
    $('#map').closest('.card').slideDown();
    this.addPlacemarks(question);
}
Austat.prototype.makeQuestion = function(){
    var austat = this;
    var topic = this.getRandomTopic();
    $.ajax({
        url: '/query/' + topic,
        success: function(q){
            console.log(!q['value'])
                var l = austat.getRandomItem(q.locations);
                q.question = Mustache.render(q.question, l)
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
    $('#question').closest('.card').slideUp(function(){
        $('#answer').closest('.card').slideDown();
    });
    var mapObj = this;
    //answer.answer.correct = false;
    //if ('answer_' + answer.answer.id === selected){
    //    answer.answer.correct = true;
    //}
    var tmpl = $('#answer-template').html();
    var html = Mustache.render(tmpl, answer);
    $('#answer').html(html);
    $('#answer #next').click(function(){
        mapObj.makeQuestion()
        $(this).closest('.card').slideUp(function(){
            $('#question').closest('.card').slideDown();
        });
    });
}

Austat.prototype.addPlacemarks = function(question){
    map = this.get_map();
    var tmpl = $('#question-template').html();
    var html = Mustache.render(tmpl, question);
    $('#mapQuestion').html(html);
    $('#question').closest('.card').prev().slideDown();
    if (this.layer){
        this.map.removeLayer(this.layer);
    }
    var mapObj = this
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
            mapObj.results(geom.value)
            $('#map').closest('.card').slideUp();
        });
        geom.openPopup();
        geom.addTo(map);
        this.layer = geom;
        map.invalidateSize()
    });
}
