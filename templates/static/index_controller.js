	
var app = angular.module("indexApp", ['ngAnimate','mm.foundation'])
.controller('TourDemoCtrl', function ($scope, $tour) {
	$scope.startTour = $tour.start;
});

