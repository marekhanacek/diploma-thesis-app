var app;

function App() {
    this.body = $('body');
    this.mapBody = $('body.map');
    this.slider = null;
    this.normalMap = null;
    this.popupMap = null;
    this.newOfferMap = null;
    this.mapHistory = null;
    this.isMapPage = null;
    this.mapPopupInit = false;
    this.mobileVersion = 'map'; // map or text

    this.el = {
        'offerTable': this.body.find('.offer-table tr'),
        'site': this.body.find('#site'),
        'cookies': this.body.find('#privacy-policy'),
        'showTextMobileButton': this.body.find('#show-text-mobile'),
        'showMapMobileButton': this.body.find('#show-map-mobile'),
        'map': this.body.find('#map'),
        'contentMap': this.body.find('#content-map')
    };

    this.init = function () {
        this.initMap();
        this.isMapPage = this.body.hasClass('map');
        if (this.isMapPage) this.mapHistory = new MapHistory(this.el.site, this.normalMap);
        this.loadPlugins();
        this.initEvents();
    };

    this.showAllOffers = function () {
        this.el.offerTable.show(1000);
        $('#show-all-offers').hide();
    };

    this.destroySlider = function () {
        this.slider.slider('destroy');
    };

    this.mapAjax = function (href, addToMapHistory) {
        var that = this;
        this.destroySlider();
        if (!this.isMapPage) return true;
        if (addToMapHistory) this.mapHistory.addPage();
        this.el.site.load(href, function () {
            that.loadPlugins();
        });
        return false;
    };

    this.mapOfferAjax = function (href, offerId) {
        var that = this;
        this.destroySlider();
        if (!this.isMapPage) return true;
        this.mapHistory.addPage();
        this.el.site.load(href, function () {
            that.normalMap.showDistance(offerId);
            that.loadPlugins();
        });
        if (this.isMobile()) {
            that.showTextMobile();
        }
        return false;
    };

    this.allowCookies = function () {
        var that = this;
        var date = new Date();
        date.setFullYear(date.getFullYear() + 10);
        document.cookie = 'cookies-allowed=1; path=/; expires=' + date.toGMTString();

        this.el.cookies.animate({
            marginBottom: -this.el.cookies.outerHeight()
        }, 500, function () {
            that.el.cookies.remove();
        });
    };

    this.loadPlugins = function () {
        var that = this;

        this.body.find('[data-toggle="tooltip"]').tooltip();

        this.body.find("#star-input input").rating({
            step: 1.0,
            showCaption: false,
            size: 'xs',
            showClear: false
        });

        if (this.body.find("#offer-slider").length) {
            this.slider = this.body.find("#offer-slider");
            this.slider.slider({
                'tooltip': "hide"
            });
            this.slider.on('change', function () {
                $('#slider-currency-from .amount').text(that.slider.slider('getValue')[0]);
                $('#slider-currency-to .amount').text(that.slider.slider('getValue')[1]);
            });
            this.slider.on('slideStop', function () {
                that.refreshOffers();
            });
        }
    };

    this.refreshOffers = function () {
        var that = this;

        $('#offers-box #offers-loading').show();
        $('#offers-box .offer-table').hide();
        this.el.site.load(
            $('#offer-frm').attr('action'),
            {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'amount_from': this.slider.slider('getValue')[0],
                'amount_to': this.slider.slider('getValue')[1],
                'currency_from': $('select[name=currency_from]').val(),
                'currency_to': $('select[name=currency_to]').val()
            },
            function () {
                $('#offers-box #offers-loading').hide();
                $('#offers-box .offer-table').show();
                that.initNormalMap();
                that.loadPlugins();
            }
        );
    };

    this.initNormalMap = function () {
        var that = this;
        this.normalMap.deleteAll();
        this.normalMap.setZoom(5);

        var position = {
            'lat': parseFloat(this.body.data('lat')),
            'lng': parseFloat(this.body.data('lng'))
        };
        var radius = this.body.data('radius') * 1000;
        this.normalMap.addMarker(position);
        this.normalMap.setCenter(position);
        this.normalMap.addCircle(radius);

        if (mapOffers != undefined) {
            $.each(mapOffers, function (key, data) {
                var offer = new Offer(data.id, data.lat, data.lng, data.amountFrom, data.amountTo, data.detailUrl, data.user, data.userVerified);
                that.normalMap.addOffer(offer);
            });
        }
    };

    this.historyBack = function () {
        this.mapHistory.previous();
        this.loadPlugins();
    };

    this.resizeMap = function () {
        this.body.toggleClass('map-hidden');
        this.el.site.toggleClass('container');
        $('#nav > div').toggleClass('container');
        $('footer').toggleClass('container');
    };

    this.offerAnimationStart = function (id) {
        this.normalMap.offers[id].marker.setAnimation(google.maps.Animation.BOUNCE);
    };

    this.offerAnimationStop = function (id) {
        this.normalMap.offers[id].marker.setAnimation(false);
    };

    this.initMap = function () {
        if ($("#map").length) {
            app.normalMap = new Map('map');
            app.initNormalMap();
        }
        if ($("#map-new-offer").length) {
            app.initNewOfferMap();
        }
        if ($("#map-preferences").length) {
            app.initPreferencesMap();
        }
    };

    this.initNewOfferMap = function () {
        this.newOfferMap = new Map('map-new-offer');
        this.newOfferMap.initSearch('map-form-new-offer');
    };

    this.initPreferencesMap = function () {
        this.newOfferMap = new Map('map-preferences');
        this.newOfferMap.initSearch('map-form-preferences', true);
    };

    this.initPopupMap = function () {
        if (this.mapPopupInit) return;

        var that = this;
        this.mapPopupInit = true;
        this.popupMap = new Map('map-popup');
        this.popupMap.resize();
        this.popupMap.initSearch('map-form-popup', true);
        this.popupMap.addMarkerByClick(function (position) {
            that.popupMap.setSearchLatLng(position.lat(), position.lng());
        });
    };

    this.recalculateAmountTo = function () {
        var currency_from = $('#map-form-new-offer select[name="currency_from"]');
        var currency_to = $('#map-form-new-offer select[name="currency_to"]');
        var amount_from = $('#map-form-new-offer input[name="amount_from"]');
        var amount_to = $('#map-form-new-offer input[name="amount_to"]');
        $.ajax({
            url: '/exchange_rate/'+currency_from.val()+'/'+currency_to.val(),
            success: function(data) {
                amount_to.val(amount_from.val() * data);
            }
        })
    };

    this.initEvents = function () {
        var that = this;

        this.body.on('click', '#map-button', function (e) {
            e.preventDefault();
            that.resizeMap();
            $(this).find('span.text').toggle();
        });

        this.body.on('shown.bs.modal', '#addressModal', function () {
            that.initPopupMap();
        });

        this.body.on('change', '#offer-frm select[name="currency_from"]', function () {
            var currency_from = $('#offer-frm select[name="currency_from"]');
            var currency_to = $('#offer-frm select[name="currency_to"]');

            if (currency_from.val() == currency_to.val()) {
                var first = $('#offer-frm select[name="currency_to"] option:nth-child(1)').val();
                var second = $('#offer-frm select[name="currency_to"] option:nth-child(2)').val();
                if (currency_from.val() == first) {
                    currency_to.val(second);
                } else {
                    currency_to.val(first);
                }
            }
            that.refreshOffers();
        });

        this.body.on('change', '#offer-frm select[name="currency_to"]', function () {
            that.refreshOffers();
        });

        this.body.on('click', '#back-button', function (e) {
            e.preventDefault();
            that.historyBack();
        });

        this.body.on('click', '#show-all-offers', function (e) {
            e.preventDefault();
            that.showAllOffers();
        });

        this.body.on('click', '#allow-cookies-button', function (e) {
            e.preventDefault();
            that.allowCookies();
        });

        this.body.on('mouseenter', "tr.map-offer-ajax", function () {
            that.offerAnimationStart($(this).data('offer-id'));
        });

        this.body.on('mouseleave', 'tr.map-offer-ajax', function () {
            that.offerAnimationStop($(this).data('offer-id'));
        });

        this.mapBody.on('click', ".map-ajax", function () {
            return that.mapAjax(
                $(this).attr('href') != undefined ? $(this).attr('href') : $(this).data('href'),
                $(this).data('history')
            );
        });

        this.mapBody.on('click', ".map-offer-ajax", function (e) {
            return that.mapOfferAjax(
                $(this).attr('href') != undefined ? $(this).attr('href') : $(this).data('href'),
                $(this).data('offer-id')
            );
        });

        this.mapBody.on('click', '#show-text-mobile', function (e) {
            e.preventDefault();
            that.showTextMobile();
        });

        this.mapBody.on('click', '#show-map-mobile', function (e) {
            e.preventDefault();
            that.showMapMobile();
        });

        this.body.on('change', '#map-form-new-offer select[name="currency_from"]', function (e) {
            var currency_from = $('#map-form-new-offer select[name="currency_from"]');
            var currency_to = $('#map-form-new-offer select[name="currency_to"]');

            if (currency_from.val() == currency_to.val()) {
                var first = $('#map-form-new-offer select[name="currency_to"] option:nth-child(1)').val();
                var second = $('#map-form-new-offer select[name="currency_to"] option:nth-child(2)').val();
                if (currency_from.val() == first) {
                    currency_to.val(second);
                } else {
                    currency_to.val(first);
                }
            }

            that.recalculateAmountTo();
        });

        this.body.on('change', '#map-form-new-offer select[name="currency_to"]', function (e) {
            var currency_from = $('#map-form-new-offer select[name="currency_from"]');
            var currency_to = $('#map-form-new-offer select[name="currency_to"]');

            if (currency_from.val() == currency_to.val()) {
                var first = $('#map-form-new-offer select[name="currency_to"] option:nth-child(1)').val();
                var second = $('#map-form-new-offer select[name="currency_to"] option:nth-child(2)').val();
                if (currency_from.val() == first) {
                    currency_from.val(second);
                } else {
                    currency_from.val(first);
                }
            }

            that.recalculateAmountTo();
        });

        this.body.on('keyup', '#map-form-new-offer input[name="amount_from"]', function (e) {
            that.recalculateAmountTo();
        });

        $(window).resize(function () {
            if (that.isMobile()) {
                that.showMobileVersion();
            } else {
                that.showDesktopVersion();
            }
        });
    };

    this.showTextMobile = function () {
        this.mobileVersion = 'text';
        this.el.showTextMobileButton.hide();
        this.el.showMapMobileButton.show();
        this.el.map.hide();
        this.el.contentMap.show();
    };

    this.showMapMobile = function () {
        this.mobileVersion = 'map';
        this.el.showTextMobileButton.show();
        this.el.showMapMobileButton.hide();
        this.el.map.show();
        this.el.contentMap.hide();
        this.normalMap.resize();
    };

    this.showDesktopVersion = function () {
        this.el.map.show();
        this.el.contentMap.show();
    };

    this.showMobileVersion = function () {
        if (this.mobileVersion == 'text') {
            this.showTextMobile()
        } else {
            this.showMapMobile()
        }
    };


    this.isMobile = function () {
        return $(window).width() < 992;
    }

}


$(document).ready(function () {
    app = new App();
    app.init();
});