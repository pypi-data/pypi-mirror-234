from djangoldp_energiepartagee.models import Contribution
from oidc_provider.views import userinfo
from django.utils.translation import gettext_lazy as _
from oidc_provider.lib.claims import ScopeClaims

class ActorsScopeClaims(ScopeClaims):
    info_moncompte = (
        _(u'Moncompte'),
        _(u'This is the custom claim providing info on all EnergiePartagee information associated with the user.'),
    )

    def scope_moncompte(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        # self.client - Client requesting this claims.
        dic = {}

        if self.user.is_authenticated:
            # Get list of related actors of current user
            from djangoldp_energiepartagee.models import Relatedactor, Contribution
            user_actors_id = Relatedactor.get_user_actors_id(user=self.user)

            # Get membership status of the actors
            activeContributions = Contribution.objects.filter(
                actor_id__in=user_actors_id,
                year = Contribution.get_current_contribution_year()
            )

            if activeContributions.__len__() > 0:
                dic = {
                    'membership': 'active',
                }
            else:
                dic = {
                    'membership': 'inactive',
                }

        return dic

    # If you want to change the description of the profile scope, you can redefine it.
    info_profile = (
        _(u'Profile'),
        _(u'Another description.'),
    )

    def scope_profile(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        # self.client - Client requesting this claims.
        dic = {}

        if self.user.is_authenticated:
            dic = {
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'name': self.user.get_full_name()
            }

        return dic
