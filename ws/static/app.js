/*
angularjs app
*/

// AngularJS Module
var app = angular.module('app', ['ngRoute', 'ngResource']);

// Acronyms service
app.factory("Acronyms", function($resource) {
  return $resource("/acronyms/:acronym");
});

// Controller
app.controller("gListCtrl", function($scope, Acronyms) {
  $scope.acronym = "";
  $scope.error = "";
  $scope.rs = [];
  $scope.search = "";

  // get list of acronyms match the input, then populate $scope.rs
  $scope.getList = function(acronym) {
    $scope.search = acronym;
    if(acronym === undefined || acronym === "") {
      $scope.error = "Please enter something to search";
      $scope.rs = [];
      return;
    }
    $scope.rs = Acronyms.query(
      {acronym: acronym},
      function(data) {
        $scope.error = "";
      },
      function(response) {
        console.log(response.status);
        if(response.status === 404)
          $scope.error = "'" + $scope.acronym + "' not found";
        else
          $scope.error = "Error occured, code: " + response.ststus;
        $scope.rs = [];
      }
    );
  };
});

