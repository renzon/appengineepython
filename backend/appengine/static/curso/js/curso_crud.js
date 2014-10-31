var crud_modulo = angular.module('curso_crud', ['curso_rest']);

crud_modulo.controller('CursoController', ['$scope', 'CursoAPI', function ($scope, CursoAPI) {
    $scope.mostrarCursoFormFlag = false;
    $scope.cursos = [];
    $scope.cursoParaEdicao = {};

    var $formEdicao = null; // jQuery

    $scope.editarCurso = function (curso) {
        $scope.cursoParaEdicao = curso;
        if ($formEdicao == null) {
            $formEdicao = $('#editform'); // jQuery
        }
        $formEdicao.modal('show');
    };

    $scope.esconderFormEdicao = function () {
        $formEdicao.modal('hide');
    };

    CursoAPI.listar().success(function (cursos) {
        $scope.cursos = cursos;
    });

    $scope.adicionarCurso = function (curso) {
        $scope.cursos.push(curso);
    };

    $scope.alterarVisibilidadeDeFormDeCurso = function () {
        $scope.mostrarCursoFormFlag = !$scope.mostrarCursoFormFlag;
    };

    $scope.removerCurso = function ($index) {
        $scope.cursos.splice($index, 1);
    }

}]);

crud_modulo.directive('cursoEditForm', function () {
    return {
        restrict: 'E',
        templateUrl: '/static/curso/html/curso_edit_form.html',
        replace: true,
        scope: {
            curso: '=',
            cursoEditadoHandler: '&'
        },
        controller: ['$scope', 'CursoAPI', function ($scope, CursoAPI) {
            $scope.cursoEditado = {};
            $scope.executandoEdicao = false;
            $scope.erros = [];

            $scope.$watch('curso', function () {
                $scope.cursoEditado.id = $scope.curso.id;
                $scope.cursoEditado.preco = $scope.curso.preco;
                $scope.cursoEditado.titulo = $scope.curso.titulo;
            });

            $scope.editar = function () {
                if (!$scope.executandoEdicao) {
                    $scope.executandoEdicao = true;
                    $scope.erros = [];

                    var promessa = CursoAPI.editar($scope.cursoEditado);

                    promessa.success(function (cursoEditado) {
                        $scope.curso.preco = cursoEditado.preco;
                        $scope.curso.titulo = cursoEditado.titulo;
                        $scope.executandoEdicao = false;
                        $scope.cursoEditadoHandler();
                    });

                    promessa.error(function (erros) {
                        $scope.erros = erros;
                        $scope.executandoEdicao = false;
                    });
                }
            }
        }]
    }
});
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
                        $scope.cursoSalvoHandler({'curso': curso_salvo});
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
        scope: {
            curso: '=',
            editarCurso: '&',
            apagarCursoHandler: '&'
        },
        controller: ['$scope', 'CursoAPI', function ($scope, CursoAPI) {
            $scope.apagandoCursoFlag=false;

            $scope.iniciarEdicao = function () {
                $scope.editarCurso({'curso': $scope.curso});
            };

            $scope.apagar = function () {
                $scope.apagandoCursoFlag=true;
                CursoAPI.apagar($scope.curso.id).success(function () {
                    $scope.apagarCursoHandler();
                }).error(function () {
                    $scope.apagandoCursoFlag=false;
                    alert('Desculpe, não foi possível apagar');
                })
            };
        }]
    }
});