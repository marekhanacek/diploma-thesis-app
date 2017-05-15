function Map(elementId) {
    this.markers = [];
    this.circles = [];
    this.lines = [];
    this.offers = {};
    this.zoom = 9;
    this.center = {lat: 50.0952, lng: 14.4023};
    this.map = new google.maps.Map(document.getElementById(elementId), {
        zoom: this.zoom,
        center: this.center,
        streetViewControl: false
    });
    this.search = {};

    this.getActualSettings = function () {
        return {
            'markers': this.markers,
            'circles': this.circles,
            'lines': this.lines,
            'offers': this.offers,
            'zoom': this.zoom,
            'center': this.center
        }
    };

    this.setZoom = function (zoom) {
        this.zoom = zoom;
        this.map.setZoom(zoom);
    };

    this.addCircle = function (radius, center) {
        center = center || this.center;

        this.circles.push(new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.5,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.1,
            map: this.map,
            center: center,
            radius: radius
        }));
    };

    this.addMarker = function (position, title) {
        title = title || '';

        this.markers.push(new google.maps.Marker({
            map: this.map,
            position: position,
            title: title
        }));
    };

    this.addLine = function (coordinates) {
        this.lines.push(new google.maps.Polyline({
            path: coordinates,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2,
            map: this.map
        }));
    };

    this.setCenter = function (center) {
        this.center = center;
        this.map.setCenter(this.center);
    };

    this.addOffer = function (offer, offerMouseOverCallback, offerMouseOutCallback) {
        var that = this;
        offer.marker.setMap(this.map);

        google.maps.event.addListener(offer.marker, 'click', function () {
            html = '<h3>' + offer.amountFrom + ' to ' + offer.amountTo + '</h3>' +
                '<h4>' + offer.user + '</h4>' +
                '<a href="' + offer.detailUrl + '" class="btn btn-my map-offer-ajax" data-offer-id="' + offer.id + '" data-history="true">Show offer details</a>';
            var infowindow = new google.maps.InfoWindow({
                content: html
            });
            infowindow.open(that.map, offer.marker);
            that.map.setCenter(offer.getPosition());
        });

        google.maps.event.addListener(offer.marker, 'mouseout', function () {
            if (offerMouseOutCallback != undefined) {
                offerMouseOutCallback(offer);
            }
        });

        google.maps.event.addListener(offer.marker, 'mouseover', function () {
            if (offerMouseOverCallback != undefined) {
                offerMouseOverCallback(offer);
            }
        });

        this.offers[offer.id] = offer;
    };


    this.deleteCircles = function () {
        this.circles.forEach(function (circle) {
            circle.setMap(null);
        });
        this.circles = [];
    };

    this.deleteMarkers = function () {
        this.markers.forEach(function (marker) {
            marker.setMap(null);
        });
        this.markers = [];
    };

    this.deleteLines = function () {
        this.lines.forEach(function (line) {
            line.setMap(null);
        });
        this.lines = [];
    };

    this.deleteOffers = function () {
        $.each(this.offers, function (id, offer) {
            offer.deleteFromMap();
        });
        this.offers = {};
    };

    this.deleteAll = function () {
        this.deleteCircles();
        this.deleteMarkers();
        this.deleteOffers();
        this.deleteLines();
    };

    this.initSearch = function (parentId, setDefault) {

        var that = this;

        this.search['parentEl'] = $('#' + parentId);
        this.search['addressInput'] = this.search['parentEl'].find('.map-address-input');
        this.search['radiusInput'] = this.search['parentEl'].find('.map-radius-input');
        this.search['latInput'] = this.search['parentEl'].find('.map-lat');
        this.search['lngInput'] = this.search['parentEl'].find('.map-lng');
        this.search['myLocationButton'] = this.search['parentEl'].find('.my-position-button');
        var searchBox = new google.maps.places.SearchBox(this.search['addressInput'][0]);

        this.map.addListener('bounds_changed', function () {
            searchBox.setBounds(that.map.getBounds());
        });

        searchBox.addListener('places_changed', function () {
            var places = searchBox.getPlaces();
            if (places.length == 0) return;

            that.deleteCircles();
            that.deleteMarkers();

            var bounds = new google.maps.LatLngBounds();
            places.forEach(function (place) {
                if (!place.geometry) {
                    console.log("Returned place contains no geometry");
                    return;
                }
                position = place.geometry.location;
                that.addMarker(position);
                that.setSearchLatLng(position.lat(), position.lng());

                if (place.geometry.viewport) {
                    bounds.union(place.geometry.viewport);
                } else {
                    bounds.extend(place.geometry.location);
                }
            });
            that.map.fitBounds(bounds);
            setCircles();
        });

        this.search['myLocationButton'].on('click', function (e) {
            e.preventDefault();
            that.setMyLocation(true, function (position) {
                var lat = position.coords.latitude;
                var lng = position.coords.longitude;
                that.address(lat, lng, function (address) {
                    that.setSearchLatLng(position.coords.latitude, position.coords.longitude);
                    that.search['addressInput'].val(address);
                });
            });
            setCircles();
            that.fitAllBounds();
        });

        this.search['radiusInput'].on('keyup mouseup', function () {
            setCircles();
            that.fitAllBounds();
        });

        setCircles = function () {
            var radius = that.search['radiusInput'].val();
            that.deleteCircles();
            that.markers.forEach(function (marker) {
                that.addCircle(radius * 1000, marker.getPosition());
            });
        };

        if (setDefault) {
            var position = {
                lat: parseFloat(this.search['latInput'].val()),
                lng: parseFloat(this.search['lngInput'].val())
            };
            that.addMarker(position);
            setCircles();
            that.fitAllBounds();
        }
    };

    this.address = function (lat, lng, callback) {
        $.ajax({
            method: "GET",
            url: 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + lat + ',' + lng + '&key=AIzaSyA8Wa05QdGga7M2mLeCJzUtpRB2U7hHE8c'
        }).done(function (data) {
            callback(data.results[0].formatted_address);
        });
    };

    this.setSearchLatLng = function (lat, lng) {
        this.search['latInput'].val(lat);
        this.search['lngInput'].val(lng);
    };

    this.addMarkerByClick = function (callback) {
        var that = this;
        this.map.addListener('click', function (event) {
            that.deleteMarkers();
            that.addMarker(event.latLng);
            callback(event.latLng);
        });
    };

    this.resize = function () {
        google.maps.event.trigger(this.map, "resize");
    };

    this.setMyLocation = function (setCenter, callback) {

        this.markers.forEach(function (marker) {
            marker.setMap(null);
        });
        this.markers = [];

        var that = this;
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                var pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                that.addMarker(pos, 'Vaše lokace');
                if (setCenter) {
                    that.map.setCenter(pos);
                    that.setZoom(18);
                }
                callback(position);
            }, function () {
                alert('Vaše poloha nebyla nalezena.');
            });
        } else {
            alert('Vaše poloha nebyla nalezena.');
        }
    };

    this.showDistance = function (id) {
        offer = this.offers[id];
        this.deleteAll();

        var userCoords = {lat: parseFloat($('body').data('lat')), lng: parseFloat($('body').data('lng'))};
        var offerCoords = offer.getPosition();

        this.addMarker(userCoords);
        this.addOffer(offer);
        this.addLine([userCoords, offerCoords]);

        var bounds = new google.maps.LatLngBounds();
        bounds.extend(userCoords);
        bounds.extend(offerCoords);
        this.map.fitBounds(bounds);
    };

    this.fitAllBounds = function (id) {
        var bounds = new google.maps.LatLngBounds();
        this.circles.forEach(function (circle) {
            bounds.union(circle.getBounds());
        });
        $.each(this.offers, function (id, offer) {
            bounds.extend(offer.marker.getPosition());
        });
        $.each(this.lines, function (id, line) {
            var points = line.getPath().getArray();
            for (var n = 0; n < points.length; n++) {
                bounds.extend(points[n]);
            }
        });
        this.map.fitBounds(bounds);
    };


    this.applySettings = function (settings) {
        that = this;
        this.deleteAll();
        this.setZoom(settings['zoom']);
        this.setCenter(settings['center']);
        settings['markers'].forEach(function (marker) {
            that.addMarker(marker.position, marker.title);
        });
        settings['circles'].forEach(function (circle) {
            that.addCircle(circle.radius, circle.center);
        });
        settings['lines'].forEach(function (line) {
            that.addLine(line.getPath());
        });
        $.each(settings['offers'], function (id, offer) {
            that.addOffer(offer);
        });
        this.fitAllBounds();
    };
}


function Offer(id, lat, lng, amountFrom, amountTo, detailUrl, user, userIsVerified) {
    this.id = id;
    this.lat = lat;
    this.lng = lng;
    this.amountFrom = amountFrom;
    this.amountTo = amountTo;
    this.detailUrl = detailUrl;
    this.user = user;
    this.userIsVerified = userIsVerified;

    this.init = function () {
        this.marker = new google.maps.Marker({
            position: this.getPosition(),
            icon: this.getMarkerImage()
        });
    };

    this.getPosition = function () {
        return {lat: lat, lng: lng};
    };

    this.getMarkerImage = function () {
        var markerUrl = this.userIsVerified ? $('body').data('marker-verified') : $('body').data('marker');
        return {
            url: markerUrl,
            size: new google.maps.Size(30, 50),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(15, 50)
        };
    };

    this.deleteFromMap = function () {
        this.marker.setMap(null)
    };

    this.init();
}

function MapHistory(element, map) {
    this.map = map;
    this.element = element;
    this.history = [];
    this.mapSettings = [];
    this.backButtonId = 'back-button';

    this.addPage = function () {
        var html = $('#site > *');
        this.deleteBackButton();
        this.history.push(html);
        this.mapSettings.push(this.map.getActualSettings());
        this.element.before(this.createBackButtonHtml());
    };

    this.previous = function () {
        this.element.html(this.history.pop());
        this.map.applySettings(this.mapSettings.pop());
        if (!this.history.length) {
            this.deleteBackButton();
        }
    };

    this.deleteBackButton = function () {
        $('#' + this.backButtonId).remove();
    };

    this.createBackButtonHtml = function () {
        return '' +
            '<a href="#" class="btn-circle" id="' + this.backButtonId + '">' +
            '<span class="circle">' +
            '<span class="glyphicon glyphicon-chevron-left"></span>' +
            '</span>' +
            'Back' +
            '</a>'
    }
}
