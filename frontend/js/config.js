// Frontend config: query params and localStorage override deployment defaults.
(function(){
  const params = new URLSearchParams(window.location.search);
  const qApi = params.get('api');
  const qMocks = params.get('mocks');
  const deploy = window.SRA_DEPLOY_CONFIG || {};
  if(qApi) localStorage.setItem('SRA_BASE_URL', qApi);
  if(qMocks !== null) localStorage.setItem('SRA_USE_MOCKS', qMocks === '1' || qMocks === 'true');

  const storedBase = localStorage.getItem('SRA_BASE_URL');
  const baseUrl = storedBase || deploy.BASE_URL || (location.hostname === 'localhost' ? 'http://localhost:8080' : `${location.origin}`);

  const storedMocks = localStorage.getItem('SRA_USE_MOCKS');
  const useMocks = storedMocks !== null
    ? storedMocks === 'true'
    : typeof deploy.USE_MOCKS === 'boolean'
      ? deploy.USE_MOCKS
      : false;

  window.SRA_CONFIG = {
    BASE_URL: baseUrl,
    USE_MOCKS: useMocks
  };
  console.debug('[SRA] CONFIG', window.SRA_CONFIG);
})();
