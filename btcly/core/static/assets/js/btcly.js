angular.module('btcly', ['mongolab']).
  config(function($routeProvider) {
    $routeProvider.
      when('/', {controller:HomeCtrl, templateUrl:'/static/html/home.tmpl'}).
      when('/resource/:resourceId', {controller:ShowResourceCtrl, templateUrl:'/static/html/show_resource.tmpl'}).
      otherwise({redirectTo:'/'});
  });
 
 
function HomeCtrl($scope, RemoteResource) {
  $scope.title = "btcly";
  $scope.projects = RemoteResource.query();
}
 
function ShowResourceCtrl($scope, $location, $routeParams, RemoteResource) {
  var self = this;
 
  RemoteResource.get({id: $routeParams.resourceId}, function(remoteResource) {
    self.original = remoteResource;
    $scope.remoteResource = new RemoteResource(self.original);
  });
 
  $scope.isClean = function() {
    return angular.equals(self.original, $scope.remoteResource);
  }
 
  $scope.destroy = function() {
    self.original.destroy(function() {
      $location.path('/list');
    });
  };
 
  $scope.save = function() {
    $scope.remoteResource.update(function() {
      $location.path('/');
    });
  };
}