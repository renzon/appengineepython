var crud_modulo=angular.module('curso_crud',[]);

crud_modulo.directive('cursoform',function(){
    return {
        restrict: 'E',
        templateUrl: '/static/curso/html/curso_form.html'
    }
});