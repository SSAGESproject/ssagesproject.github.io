
angular.module('FloryApp', ['mm.foundation'])

//This controller defines the actual logistics of the modal instance
.controller('ModalDemoCtrl', function ($scope, $modal, $log) {

	$scope.open = function () {

		// details of the modal instance
		var modalInstance = $modal.open({
			templateUrl: 'myModalContent',
			controller: 'ModalInstanceCtrl'
		});

		modalInstance.result.then(function (selectedItem) {
			$scope.selected = selectedItem;
		}, function () {
			$log.info('Modal dismissed at: ' + new Date());
		});
	};
})

//This controller IS the instance
// Don't need any angular inside so it is blank
.controller('ModalInstanceCtrl', function ($scope, $modalInstance) {


});
