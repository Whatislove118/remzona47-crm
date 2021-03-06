from rest_framework import routers

from api.apps.analytics.views import AnalyticsJobsViewSet, AnalyticsUserWorklogsViewSet

router = routers.SimpleRouter()
router.register(r"analytics/worklogs", AnalyticsUserWorklogsViewSet)
router.register(r"analytics/jobs", AnalyticsJobsViewSet)
