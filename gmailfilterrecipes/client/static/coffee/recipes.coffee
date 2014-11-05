recipesApp = angular.module('recipesApp', [])

recipesApp.controller 'RecipesController', ($scope, $http, $window) ->
  $scope.recipeSetJson = ''
  $scope.show = false

  $http.get('/filters.json').success (data) ->
    $scope.recipeSet = data
    $scope.recipeSetJson = angular.toJson data, true

  $scope.filtersXml = ''
  $scope.refreshFiltersXml = ->
    $http.post('/filters.xml', $scope.recipeSet).success (data) ->
      $scope.filtersXml = data
  $scope.downloadFiltersXml = ->
    $scope.filtersXml = ''
    $window.post('/filters.xml?', $scope.recipeSet)
  $scope.updateForm = ->
    $scope.recipeSet = JSON.parse $scope.recipeSetJson
  $scope.updateRecipe = ->
    $scope.recipeSetJson = angular.toJson $scope.recipeSet, true
  $scope.showRecipe = ->
    $scope.show = true
  $scope.selectAll = (value) ->
    # value should be true or false
    for recipe in $scope.recipeSet.recipes
      recipe.selected = value