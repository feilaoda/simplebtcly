angular.module('mongolab', ['ngResource']).
    factory('RemoteResource', function($resource) {
      var RemoteResource = $resource('https://api.mongolab.com/api/1/databases' +
          '/angularjs/collections/projects/:id',
          { apiKey: '4f847ad3e4b08a2eed5f3b54' }, {
            update: { method: 'PUT' }
          }
      );
 
      RemoteResource.prototype.update = function(cb) {
        return RemoteResource.update({id: this._id.$oid},
            angular.extend({}, this, {_id:undefined}), cb);
      };
 
      RemoteResource.prototype.destroy = function(cb) {
        return RemoteResource.remove({id: this._id.$oid}, cb);
      };
 
      return RemoteResource;
    });