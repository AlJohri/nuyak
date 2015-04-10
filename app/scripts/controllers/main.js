'use strict';

/**
 * @ngdoc function
 * @name nuyakApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the nuyakApp
 */
angular.module('nuyakApp')
  .controller('MainCtrl', function ($scope, Ref, $firebaseArray) {
    $scope.yaks = $firebaseArray(Ref.child('yaks').limitToLast(1000));
    $scope.yaks.$loaded().catch(alert);

    function alert(msg) {
      $scope.err = msg;
      $timeout(function() {
        $scope.err = null;
      }, 5000);
    }

  });
