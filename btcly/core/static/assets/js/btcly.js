angular.module('project', [remoteResource]).
    config(function($routeProvider) {
        $routeProvider.
        when('/', {controller:HomeCtrl, templateUrl:'/static/html/home.html'}).
        when('/resource/:resourceId', {controller:ResourceCtrl, templateUrl:'/static/html/show_resource.html'}).
        otherwise({redirectTo:'/'});
    });
 

angular.module('remoteResource', ['ngResource']).
    factory('Resource', function($resource) {
        var Resource = $resource('https://api.mongolab.com/api/1/databases' +
        '/btcly/collections/resources/:id',
        { apiKey: 'bX5BE5VaiHJH0NMqsaxBQAEiPKHJQ86K' }, 
        { update: { method: 'GET' } }
        );
        return Resource;
    });

