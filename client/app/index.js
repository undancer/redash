import ngModule from '@/config';
import messages from '@/locales/zh';

ngModule.config(($locationProvider, $compileProvider, uiSelectConfig, $translateProvider) => {
  $compileProvider.debugInfoEnabled(false);
  $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|data|tel|sms|mailto):/);
  $locationProvider.html5Mode(true);
  uiSelectConfig.theme = 'bootstrap';

  $translateProvider.useSanitizeValueStrategy(null);
  $translateProvider.translations('zh', messages);
  $translateProvider.preferredLanguage('zh');
});

// Update ui-select's template to use Font-Awesome instead of glyphicon.
ngModule.run(($templateCache) => {
  const templateName = 'bootstrap/match.tpl.html';
  let template = $templateCache.get(templateName);
  template = template.replace('glyphicon glyphicon-remove', 'fa fa-remove');
  $templateCache.put(templateName, template);
});

export default ngModule;
