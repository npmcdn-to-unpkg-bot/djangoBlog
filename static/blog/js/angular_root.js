/**
 * Created by zhaochy on 16-5-26.
 */
var app = angular.module('blog', ['ngRoute']).config(function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
}).config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('$$');
    $interpolateProvider.endSymbol('$$');
});

// app.config(['$routeProvider',function ($routeProvider) {
//     $routeProvider
//         .when('/login',{controller:'NavbarController',templateUrl:'/static/blog/login.html'})
// }])
