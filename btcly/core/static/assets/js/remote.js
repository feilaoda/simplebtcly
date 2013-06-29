angular.module('remote', ['ngResource']).
    factory('RemoteResource', function($resource) {
      var RemoteResource = $resource('http://api.btcly.com/v1/btcly/resources/:resourceId',
          { apiKey: '4f847ad3e4b08a2eed5f3b54' }
      );
      return RemoteResource;
    });