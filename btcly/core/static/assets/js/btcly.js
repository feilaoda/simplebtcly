angular.module('btcly', ['remote'], function ($compileProvider) {
  $compileProvider.urlSanitizationWhitelist(/^\s*(https?|ftp|mailto|file|magnet|ed2k|thunder):/);
}
).
  config(function($routeProvider) {
    $routeProvider.
      when('/', {controller:HomeCtrl, templateUrl:'/static/html/home.html'}).
      when('/resource/:resourceId', {controller:ShowResourceCtrl, templateUrl:'/static/html/show_resource.html'}).
      otherwise({redirectTo:'/'});
  });
 

 
function HomeCtrl($scope, RemoteResource) {
  $scope.resources = RemoteResource.query();
  $scope.title = $scope.resources.title;
  $scope.links = $scope.resources.links
}
 
function ShowResourceCtrl($scope, $location, $routeParams, RemoteResource) {
  var self = this;
 
  RemoteResource.get({id: $routeParams.resourceId}, function(remoteResource) {
    self.original = remoteResource;
    $scope.remoteResource = new RemoteResource(self.original);

  });
}