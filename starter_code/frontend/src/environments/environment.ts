/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://dev-gys4qzsrt6aecaks.us.auth0.com/oauth/token', // the running FLASK api server url
  auth0: {
    url: 'dev-gys4qzsrt6aecaks.us.auth0.com', // the auth0 domain prefix
    audience: 'https://dev-gys4qzsrt6aecaks', // the audience set for the auth0 app
    clientId: 'hqTXRg9f5W8URCCIxN4l4cMQwsMgMGsV', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:5000/', // the base url of the running ionic application. 
  }
};
