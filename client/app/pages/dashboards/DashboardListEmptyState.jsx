import React from 'react';
import PropTypes from 'prop-types';
import { BigMessage } from '@/components/BigMessage';
import { NoTaggedObjectsFound } from '@/components/NoTaggedObjectsFound';
import { EmptyState } from '@/components/empty-state/EmptyState';
import { getMessage as _ } from '@/lib/locales';

export default function DashboardListEmptyState({ page, searchTerm, selectedTags }) {
  if (searchTerm !== '') {
    return (
      <BigMessage message={_('Sorry, we couldn\'t find anything.')} icon="fa-search" />
    );
  }
  if (selectedTags.length > 0) {
    return (
      <NoTaggedObjectsFound objectType="dashboards" tags={selectedTags} />
    );
  }
  switch (page) {
    case 'favorites': return (
      <BigMessage message={_('Mark dashboards as Favorite to list them here.')} icon="fa-star" />
    );
    default: return (
      <EmptyState
        icon="zmdi zmdi-view-quilt"
        description="See the big picture"
        illustration="dashboard"
        helpLink="http://help.xinniuren.cn/bigdata/dashboard.html"
        showDashboardStep
      />
    );
  }
}

DashboardListEmptyState.propTypes = {
  page: PropTypes.string.isRequired,
  searchTerm: PropTypes.string.isRequired,
  selectedTags: PropTypes.array.isRequired, // eslint-disable-line react/forbid-prop-types
};
