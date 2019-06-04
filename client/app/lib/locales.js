import { addLocaleData, IntlProvider } from 'react-intl';

import en from 'react-intl/locale-data/en';
import zh from 'react-intl/locale-data/zh';
import messages from '@/locales/zh';

addLocaleData([...en, ...zh]);

const intlProvider = new IntlProvider({
  locale: 'zh',
  messages,
}, {});


const { intl } = intlProvider.getChildContext();

function getMessage(text) {
  return intl.formatMessage({ id: text });
}


// eslint-disable-next-line import/prefer-default-export
export { getMessage };
