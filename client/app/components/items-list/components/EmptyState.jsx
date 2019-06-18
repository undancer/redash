import React from 'react';
import { BigMessage } from '@/components/BigMessage';
import { getMessage as _ } from '@/lib/locales';

// Default "list empty" message for list pages
export default function EmptyState(props) {
  return (
    <div className="text-center">
      <BigMessage icon="fa-search" message={_('Sorry, we couldn\'t find anything.')} {...props} />
    </div>
  );
}
