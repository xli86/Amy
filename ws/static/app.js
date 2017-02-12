/*
angularjs app
*/

// AngularJS Module
var app = angular.module('app', ['ngRoute', 'ngResource']);

// register services
app.factory("Acronyms", function($resource) {
  return $resource("/acronyms/:acronym");
});
app.factory("Stats", function($resource) {
  return $resource("/stats/:key");
});

// Controller
app.controller("gListCtrl", function($scope, Acronyms, Stats) {
  $scope.acronym = "";
  $scope.error = "";
  $scope.rs = [];
  $scope.topMin = [];
  $scope.topWeek = [];
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

  // get stats info
  $scope.getStatMin = function(key, r) {
    Stats.query(
      {key: key},
      function(data) {
        r.length = 0;
        r.push.apply(r, data);
      },
      function(response) {
        console.log("get " + key + " response " + response.status);
        r.length = 0;
      }
    );
  };
  
  $scope.getStatMin('topMin', $scope.topMin);
  $scope.getStatMin('topWeek', $scope.topWeek);

});

