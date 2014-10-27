recipesApp = angular.module('recipesApp', [])

recipesApp.controller 'RecipesController', ($scope, $http, $window) ->
  $http.get('/filters.json').success (data) ->
    $scope.recipeSet = data

  $scope.filtersXml = ''
  $scope.refreshFiltersXml = ->
    $http.post('/filters.xml', $scope.recipeSet).success (data) ->
      $scope.filtersXml = data
  $scope.downloadFiltersXml = ->
    $scope.filtersXml = ''
    $window.post('/filters.xml?', $scope.recipeSet)

  $scope.selectAll = (value) ->
    # value should be true or false
    for recipe in $scope.recipeSet.recipes
      recipe.selected = value