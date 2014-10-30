var crud_modulo = angular.module('curso_crud', ['curso_rest']);

crud_modulo.controller('CursoController', ['$scope', 'CursoAPI', function ($scope, CursoAPI) {
    $scope.mostrarCursoFormFlag = false;
    $scope.cursos = [];

    CursoAPI.listar().success(function (cursos) {
        $scope.cursos = cursos;
    });

    $scope.adicionarCurso=function (curso){
        $scope.cursos.push(curso);
    };

    $scope.alterarVisibilidadeDeFormDeCurso = function () {
        $scope.mostrarCursoFormFlag = !$scope.mostrarCursoFormFlag;
    };
}]);

crud_modulo.directive('cursoform', function () {
    return {
        restrict: 'E',
        templateUrl: '/static/curso/html/curso_form.html',
        replace: true,
        scope: { cursoSalvoHandler: '&' },
        controller: ['$scope', 'CursoAPI', function ($scope, CursoAPI) {
            $scope.curso = {titulo: "", preco: ""};
            $scope.executandoSalvamento = false;
            $scope.erros = [];

            $scope.salvar = function () {
                if (!$scope.executandoSalvamento) {
                    $scope.executandoSalvamento = true;
                    $scope.erros = [];

                    var promessa = CursoAPI.salvar($scope.curso);

                    promessa.success(function (curso_salvo) {
                        console.log(curso_salvo);
                        $scope.curso = {titulo: "", preco: ""};
                        $scope.executandoSalvamento = false;
                        $scope.cursoSalvoHandler({'curso':curso_salvo});
                    });

                    promessa.error(function (erros) {
                        $scope.erros = erros;
                        $scope.executandoSalvamento = false;
                    });
                }
            }
        }]
    }
});

crud_modulo.directive('cursolinha', function () {
    return {
        restrict: 'A',
        replace: true,
        templateUrl: '/static/curso/html/curso_linha.html',
        scope: {curso: '='}
    }
});