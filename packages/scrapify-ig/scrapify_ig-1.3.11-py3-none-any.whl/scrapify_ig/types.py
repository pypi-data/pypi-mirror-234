from typing import Optional
from abc import ABC, abstractmethod

from pydantic import BaseModel

from . import exceptions

__all__ = [
    "User",
    "FollowersChunk",
    "MediaPost",
    "MediaPostsChunk",
    "CommentsChunk",
    "CommentsThreadChunk",
    "SimilarAccounts",
    "MediaPostsHashtagChunk",
    "TaggedMediaPostsChunk",
    "SearchResult",
]


class CountDict(BaseModel):
    count: Optional[int] = None


class NextChunkInterface(ABC):

    class Meta:
        __client_object = None  # Used to access the client object from inside the base models

    @abstractmethod
    def has_next_chunk(self):
        raise NotImplementedError("Method has_next_chunk must be implemented")

    @abstractmethod
    def next_chunk(self, *args, **kwargs):
        raise NotImplementedError("Method next_chunk must be implemented")

    def set_client(self, client):
        raise NotImplementedError("Method set_client must be implemented")

    def get_client(self):
        raise NotImplementedError("Method get_client must be implemented")

    @property
    def meta(self) -> "Meta":
        return self.Meta


class NextChunkMixin(NextChunkInterface):
    """
    @DynamicAttrs
    """
    def has_next_chunk(self) -> bool:
        """ Returns True if pagination_token exists, otherwise returns False """
        return bool(self.pagination_token)

    def next_chunk(self, *args, **kwargs):
        raise NotImplementedError("Method next_chunk must be implemented")

    def check_next_chunk(self, *args, **kwargs):
        """
        Throws the NoNextPageError exception if there is no pagination_token for the next page.
        Nothing does if there is a next page (there is pagination_token).
        """
        if not self.has_next_chunk():
            raise exceptions.NoNextPageError()

    def set_client(self, client):
        """ Assigns the client object to the Meta class """
        self.meta.__client_object = client

    def get_client(self):
        """ Get the client object from the Meta class """
        return self.meta.__client_object


class UserItemMixin(object):
    """
    @DynamicAttrs
    """

    def get_followers_chunk(self, client, amount: int = 50, pagination_token: str = None) -> "FollowersChunk":
        """
        This method calls the client.get_followers_chunk method.
        See the documentation for this method in the Client or UserMixin class
        """
        return client.get_followers_chunk(
            username_or_id_or_url=self.username,
            amount=amount,
            pagination_token=pagination_token
        )

    def get_user_medias_chunk(self, client, pagination_token: str = None) -> "MediaPostsChunk":
        """
        This method calls the client.get_user_medias_chunk method.
        See the documentation for this method in the Client or UserMixin class
        """
        return client.get_user_medias_chunk(
            username_or_id_or_url=self.username,
            pagination_token=pagination_token
        )


class ActiveStandaloneFundraiser(BaseModel):
    fundraisers: list = []
    total_count: int = 0


class AvatarStatus(BaseModel):
    has_avatar: Optional[bool] = None


class BioLink(BaseModel):
    click_id: Optional[str] = None
    link_id: Optional[int] = None
    link_type: Optional[str] = None
    lynx_url: Optional[str] = None
    open_external_url_with_in_app_browser: Optional[bool] = None
    title: Optional[str] = None
    url: Optional[str] = None


class UserEntity(BaseModel, UserItemMixin):
    id: Optional[int] = None
    username: Optional[str] = None


class Entity(BaseModel):
    user: Optional[UserEntity] = None


class BiographyWithEntities(BaseModel):
    entities: Optional[list[Entity]] = None
    raw_text: Optional[str] = None


class CreatorShoppingInfo(BaseModel):
    linked_merchant_accounts: Optional[list] = None


class FanClubInfo(BaseModel):
    autosave_to_exclusive_highlight: Optional[str | bool] = None
    connected_member_count: Optional[int] = None
    fan_club_id: Optional[int | str] = None
    fan_club_name: Optional[str] = None
    fan_consideration_page_revamp_eligiblity: Optional[dict] = None
    has_enough_subscribers_for_ssc: Optional[bool] = None
    is_fan_club_gifting_eligible: Optional[bool] = None
    is_fan_club_referral_eligible: Optional[bool] = None
    subscriber_count: Optional[int] = None


class ProfilePicUrlInfo(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None
    url: Optional[str] = None


class ChannelInfo(BaseModel):
    has_public_channels: Optional[bool] = None
    pinned_channels_list: Optional[list] = None


class ShortUser(BaseModel, UserItemMixin):
    full_name: Optional[str] = None
    id: Optional[str | int] = None
    is_private: Optional[bool] = None
    is_verified: Optional[bool] = None
    profile_pic_id: Optional[str | int] = None
    profile_pic_url: Optional[str] = None
    username: Optional[str] = None


class PreviewUser(BaseModel):
    id: Optional[int | str] = None
    profile_pic_url: Optional[str] = None


class ProfileContextLinkWithId(BaseModel, UserItemMixin):
    start: Optional[int] = None
    end: Optional[int] = None
    username: Optional[str] = None


class RecsFromFriends(BaseModel):
    enable_recs_from_friends: Optional[bool] = None
    recs_from_friends_entry_point_type: Optional[str] = None


class User(BaseModel, UserItemMixin):
    account_badges: Optional[list] = None
    account_category: Optional[str] = None
    account_type: Optional[int] = None
    active_standalone_fundraisers: Optional[ActiveStandaloneFundraiser] = None
    address_street: Optional[str] = None
    ads_incentive_expiration_date: Optional[int] = None
    ads_page_id: Optional[int] = None
    ads_page_name: Optional[str] = None
    auto_expand_chaining: Optional[bool] = None
    avatar_status: AvatarStatus = None
    bio_links: Optional[list[BioLink]] = None
    biography: Optional[str] = None
    biography_with_entities: Optional[BiographyWithEntities] = None
    birthday_today_visibility_for_viewer: Optional[str] = None
    business_contact_method: Optional[str] = None
    can_add_fb_group_link_on_profile: Optional[bool] = None
    can_hide_category: Optional[bool] = None
    can_hide_public_contacts: Optional[bool] = None
    can_use_affiliate_partnership_messaging_as_brand: Optional[bool] = None
    can_use_affiliate_partnership_messaging_as_creator: Optional[bool] = None
    can_use_branded_content_discovery_as_brand: Optional[bool] = None
    can_use_branded_content_discovery_as_creator: Optional[bool] = None
    category: Optional[str] = None
    category_id: Optional[int] = None
    city_id: Optional[int] = None
    city_name: Optional[str] = None
    contact_phone_number: Optional[str] = None
    creator_shopping_info: Optional[CreatorShoppingInfo] = None
    current_catalog_id: Optional[int] = None
    direct_messaging: Optional[str] = None
    displayed_action_button_partner: Optional[str] = None
    displayed_action_button_type: Optional[str] = None
    existing_user_age_collection_enabled: Optional[bool] = None
    external_lynx_url: Optional[str] = None
    external_url: Optional[str] = None
    fan_club_info: Optional[FanClubInfo] = None
    fb_page_call_to_action_id: Optional[str] = None
    fbid_v2: Optional[str] | Optional[int] = None
    feed_post_reshare_disabled: Optional[bool] = None
    follow_friction_type: Optional[int] = None
    follower_count: Optional[int] = None
    following_count: Optional[int] = None
    following_tag_count: Optional[int] = None
    full_name: Optional[str] = None
    has_anonymous_profile_picture: Optional[bool] = None
    has_chaining: Optional[bool] = None
    has_exclusive_feed_content: Optional[bool] = None
    has_fan_club_subscriptions: Optional[bool] = None
    has_guides: Optional[bool] = None
    has_highlight_reels: Optional[bool] = None
    has_igtv_series: Optional[bool] = None
    has_music_on_profile: Optional[bool] = None
    has_private_collections: Optional[bool] = None
    has_public_tab_threads: Optional[bool] = None
    has_videos: Optional[bool] = None
    hd_profile_pic_url_info: Optional[ProfilePicUrlInfo] = None
    hd_profile_pic_versions: Optional[list[ProfilePicUrlInfo]] = None
    highlight_reshare_disabled: Optional[bool] = None
    id: Optional[str] | Optional[int] = None
    include_direct_blacklist_status: Optional[bool] = None
    instagram_location_id: Optional[str] | Optional[int] = None
    interop_messaging_user_fbid: Optional[int] = None
    is_bestie: Optional[bool] = None
    is_business: Optional[bool] = None
    is_call_to_action_enabled: Optional[bool] = None
    is_category_tappable: Optional[bool] = None
    is_direct_roll_call_enabled: Optional[bool] = None
    is_eligible_for_lead_center: Optional[bool] = None
    is_eligible_for_smb_support_flow: Optional[bool] = None
    is_experienced_advertiser: Optional[bool] = None
    is_favorite: Optional[bool] = None
    is_favorite_for_clips: Optional[bool] = None
    is_favorite_for_highlights: Optional[bool] = None
    is_favorite_for_igtv: Optional[bool] = None
    is_favorite_for_stories: Optional[bool] = None
    is_in_canada: Optional[bool] = None
    is_interest_account: Optional[bool] = None
    is_memorialized: Optional[bool] = None
    is_new_to_instagram: Optional[bool] = None
    is_opal_enabled: Optional[bool] = None
    is_potential_business: Optional[bool] = None
    is_private: Optional[bool] = None
    is_profile_audio_call_enabled: Optional[bool] = None
    is_profile_broadcast_sharing_enabled: Optional[bool] = None
    is_profile_picture_expansion_enabled: Optional[bool] = None
    is_regulated_c18: Optional[bool] = None
    is_remix_setting_enabled_for_posts: Optional[bool] = None
    is_secondary_account_creation: Optional[bool] = None
    is_supervision_features_enabled: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_whatsapp_linked: Optional[bool] = None
    latitude: Optional[float] = None
    lead_details_app_id: Optional[str] = None
    live_subscription_status: Optional[str] = None
    longitude: Optional[float] = None
    media_count: Optional[int] = None
    merchant_checkout_style: Optional[str] = None
    mini_shop_seller_onboarding_status: Optional[str] = None
    mutual_followers_count: Optional[int] = None
    nametag: Optional[str] = None
    num_of_admined_pages: Optional[int] = None
    open_external_url_with_in_app_browser: Optional[bool] = None
    page_id: Optional[int] = None
    page_name: Optional[str] = None
    pinned_channels_info: Optional[ChannelInfo] = None
    primary_profile_link_type: Optional[int] = None
    professional_conversion_suggested_account_type: Optional[int] = None
    profile_context: Optional[str] = None
    profile_context_facepile_users: Optional[list[ShortUser]] = None
    profile_context_links_with_user_ids: Optional[list[ProfileContextLinkWithId]] = None
    profile_context_mutual_follow_ids: Optional[list[int]] = None
    profile_pic_id: Optional[str] = None
    profile_pic_url: Optional[str] = None
    profile_type: Optional[int] = None
    pronouns: Optional[list] = None
    public_email: Optional[str] = None
    public_phone_country_code: Optional[str] = None
    public_phone_number: Optional[str] = None
    recs_from_friends: Optional[dict] = None
    remove_message_entrypoint: Optional[bool] = None
    request_contact_enabled: Optional[bool] = None
    seller_shoppable_feed_type: Optional[str] = None
    shopping_post_onboard_nux_type: Optional[str] = None
    should_show_category: Optional[bool] = None
    should_show_public_contacts: Optional[bool] = None
    show_account_transparency_details: Optional[bool] = None
    show_fb_link_on_profile: Optional[bool] = None
    show_fb_page_link_on_profile: Optional[bool] = None
    show_ig_app_switcher_badge: Optional[bool] = None
    show_post_insights_entry_point: Optional[bool] = None
    show_shoppable_feed: Optional[bool] = None
    show_text_post_app_badge: Optional[bool] = None
    show_text_post_app_switcher_badge: Optional[bool] = None
    show_together_pog: Optional[bool] = None
    smb_delivery_partner: Optional[str] = None
    smb_support_delivery_partner: Optional[str] = None
    smb_support_partner: Optional[str] = None
    text_post_app_badge_label: Optional[str] = None
    text_post_app_joiner_number: Optional[int] = None
    text_post_app_joiner_number_label: Optional[str] = None
    third_party_downloads_enabled: Optional[int] = None
    total_ar_effects: Optional[int] = None
    total_clips_count: Optional[int] = None
    total_igtv_videos: Optional[int] = None
    transparency_product_enabled: Optional[bool] = None
    upcoming_events: Optional[list] = None
    username: Optional[str] = None
    zip: Optional[str] = None


class FollowersData(BaseModel):
    count: Optional[int] = None
    items: Optional[list[ShortUser]] = None


class FollowersChunk(BaseModel, NextChunkMixin):
    user_identifier: Optional[str] = None
    amount: Optional[int] = 50
    data: Optional[FollowersData] = None
    pagination_token: Optional[str] = None

    def __init__(self, *args, client, **kwargs):
        self.set_client(client)
        super().__init__(*args, **kwargs)

    def next_chunk(self) -> "FollowersChunk":
        """
        This method calls the client.get_followers_chunk method.
        See the documentation for this method in the Client or UserMixin class
        """
        self.check_next_chunk()
        client = self.get_client()
        return client.get_followers_chunk(
            username_or_id_or_url=self.user_identifier,
            amount=self.amount,
            pagination_token=self.pagination_token
        )


class MediaPostUser(BaseModel, UserItemMixin):
    account_badges: Optional[list] = None
    fan_club_info: Optional[FanClubInfo] = None
    fbid_v2: Optional[str | int] = None
    feed_post_reshare_disabled: Optional[bool] = None
    full_name: Optional[str] = None
    has_anonymous_profile_picture: Optional[bool] = None
    id: Optional[str | int] = None
    is_favorite: Optional[bool] = None
    is_private: Optional[bool] = None
    is_unpublished: Optional[bool] = None
    is_verified: Optional[bool] = None
    latest_reel_media: Optional[int | str] = None
    profile_pic_id: Optional[str] = None
    profile_pic_url: Optional[str] = None
    show_account_transparency_details: Optional[bool] = None
    third_party_downloads_enabled: Optional[int] = None
    transparency_product_enabled: Optional[bool] = None
    username: Optional[str] = None


class CommentInformTreatment(BaseModel):
    action_type: Optional[str | int] = None
    should_have_inform_treatment: Optional[bool] = None
    text: Optional[str] = None
    url: Optional[str] = None


class FundraiserTag(BaseModel):
    has_standalone_fundraiser: Optional[bool] = None


class MediaPostCaption(BaseModel):
    content_type: Optional[str] = None
    created_at: Optional[int] = None
    created_at_utc: Optional[int] = None
    did_report_as_spam: Optional[bool] = None
    id: Optional[int | str] = None
    is_covered: Optional[bool] = None
    is_ranked_comment: Optional[bool] = None
    pk: Optional[str | int] = None
    private_reply_status: Optional[int] = None
    share_enabled: Optional[bool] = None
    status: Optional[str] = None
    text: Optional[str] = None
    type: Optional[int] = None
    user: Optional[MediaPostUser] = None
    user_id: Optional[int | str] = None


class MediaPostImageVersionItem(BaseModel):
    estimated_scans_sizes: Optional[list[int]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    scans_profile: Optional[str] = None
    url: Optional[str] = None


class MediaPostImageVersions(BaseModel):
    items: Optional[list[MediaPostImageVersionItem]] = None


class MashupInfo(BaseModel):
    can_toggle_mashups_allowed: Optional[bool] = None
    formatted_mashups_count: Optional[int] = None
    has_been_mashed_up: Optional[bool] = None
    has_nonmimicable_additional_audio: Optional[bool] = None
    is_creator_requesting_mashup: Optional[bool] = None
    is_light_weight_check: Optional[bool] = None
    is_pivot_page_available: Optional[bool] = None
    mashup_type: Optional[int | str] = None
    mashups_allowed: Optional[bool] = None
    non_privacy_filtered_mashups_media_count: Optional[int] = None
    original_media: Optional[int | str] = None
    privacy_filtered_mashups_media_count: Optional[int] = None


class MusicMetadata(BaseModel):
    audio_type: Optional[int | str] = None
    music_canonical_id: Optional[int | str] = None
    music_info: Optional[dict] = None
    original_sound_info: Optional[dict] = None
    pinned_media_ids: Optional[list[int | str]] = None


class SharingFrictionInfo(BaseModel):
    bloks_app_url: Optional[str] = None
    sharing_friction_payload: Optional[str | dict] = None
    should_have_sharing_friction: Optional[bool] = None


class UserTagsInItem(BaseModel):
    categories: Optional[list[str]] = None
    duration_in_video_in_sec: Optional[int] = None
    position: Optional[list[float]] = None
    show_category_of_user: Optional[bool] = None
    start_time_in_video_in_sec: Optional[int] = None
    user: Optional[ShortUser] = None


class MediaPostItemMixin(object):
    """
    @DynamicAttrs
    """

    def get_media_comments_chunk(self, client, pagination_token: str = None) -> "CommentsChunk":
        """
        This method calls the client.get_media_comments_chunk method.
        See the documentation for this method in the Client or MediaPostMixin class
        """
        return client.get_media_comments_chunk(
            code_or_id_or_url=self.code,
            pagination_token=pagination_token
        )


class Location(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    external_source: Optional[str] = None
    facebook_places_id: Optional[int | str] = None
    has_viewer_saved: Optional[bool] = None
    is_eligible_for_guides: Optional[bool] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    name: Optional[str] = None
    pk: Optional[int | str] = None
    short_name: Optional[str] = None


class VideoVersion(BaseModel):
    height: Optional[int] = None
    id: Optional[str | int] = None
    type: Optional[int | str] = None
    url: Optional[str] = None
    width: Optional[int] = None


class CarouselItem(BaseModel):
    carousel_parent_id: Optional[str] = None
    commerciality_status: Optional[str] = None
    explore_pivot_grid: Optional[bool] = None
    featured_products: Optional[list] = None
    id: Optional[str] = None
    image_versions: Optional[MediaPostImageVersions] = None
    media_type: Optional[int | str] = None
    original_height: Optional[int] = None
    original_width: Optional[int] = None
    pk: Optional[int] = None
    preview: Optional[str] = None
    product_suggestions: Optional[list] = None
    play_count: Optional[int] = None
    product_type: Optional[str] = None
    sharing_friction_info: Optional[SharingFrictionInfo] = None
    shop_routing_user_id: Optional[int | str] = None
    taken_at: Optional[int] = None
    usertags: Optional[dict[str, list[UserTagsInItem]]] = None
    video_codec: Optional[str] = None
    video_duration: Optional[float] = None
    video_versions: Optional[list[VideoVersion]] = None


class AchievementsInfo(BaseModel):
    num_earned_achievements: Optional[int] = None
    show_achievements: Optional[bool] = None


class AudioReattributionInfo(BaseModel):
    should_allow_restore: Optional[bool] = None


class AdditionalAudioInfo(BaseModel):
    additional_audio_username: Optional[str] = None
    audio_reattribution_info: Optional[AudioReattributionInfo] = None


class AudioRankingInfo(BaseModel):
    best_audio_cluster_id: Optional[str | int] = None


class BrandedContentTagInfo(BaseModel):
    can_add_tag: Optional[bool] = None


class MusicAssetInfo(BaseModel):
    allows_saving: Optional[bool] = None
    artist_id: Optional[str | int] = None
    audio_asset_id: Optional[str | int] = None
    audio_cluster_id: Optional[str | int] = None
    cover_artwork_thumbnail_uri: Optional[str] = None
    cover_artwork_uri: Optional[str] = None
    dark_message: Optional[str] = None
    display_artist: Optional[str] = None
    duration_in_ms: Optional[int] = None
    fast_start_progressive_download_url: Optional[str] = None
    has_lyrics: Optional[bool] = None
    highlight_start_times_in_ms: Optional[list[int]] = None
    id: Optional[str | int] = None
    ig_username: Optional[str] = None
    is_eligible_for_audio_effects: Optional[bool] = None
    is_explicit: Optional[bool] = None
    progressive_download_url: Optional[str] = None
    reactive_audio_download_url: Optional[str] = None
    sanitized_title: Optional[str] = None
    subtitle: Optional[str] = None
    title: Optional[str] = None
    web_30s_preview_download_url: Optional[str] = None


class AudioMutingInfo(BaseModel):
    allow_audio_editing: Optional[bool] = None
    mute_audio: Optional[bool] = None
    mute_reason_str: Optional[str] = None
    show_muted_audio_toast: Optional[bool] = None


class IgArtist(ShortUser):
    pass


class MusicConsumptionInfo(BaseModel):
    allow_media_creation_with_music: Optional[bool] = None
    audio_asset_start_time_in_ms: Optional[int] = None
    audio_filter_infos: Optional[list] = None
    audio_muting_info: Optional[AudioMutingInfo] = None
    derived_content_id: Optional[str | int] = None
    display_labels: Optional[str | list] = None
    formatted_clips_media_count: Optional[int] = None
    ig_artist: Optional[IgArtist] = None
    is_bookmarked: Optional[bool] = None
    is_trending_in_clips: Optional[bool] = None
    overlap_duration_in_ms: Optional[int] = None
    placeholder_profile_pic_url: Optional[str] = None
    should_allow_music_editing: Optional[bool] = None
    should_mute_audio: Optional[bool] = None
    should_mute_audio_reason: Optional[str] = None
    should_mute_audio_reason_type: Optional[str | int] = None
    trend_rank: Optional[str | int | float] = None


class MusicInfo(BaseModel):
    music_asset_info: Optional[MusicAssetInfo] = None
    music_canonical_id: Optional[str | int] = None
    music_consumption_info: Optional[MusicConsumptionInfo] = None


class ClipsMetadata(BaseModel):
    achievements_info: Optional[AchievementsInfo] = None
    additional_audio_info: Optional[AdditionalAudioInfo] = None
    asset_recommendation_info: Optional[dict] = None
    audio_ranking_info: Optional[AudioRankingInfo] = None
    audio_type: Optional[str] = None
    branded_content_tag_info: Optional[BrandedContentTagInfo] = None
    breaking_content_info: Optional[dict] = None
    breaking_creator_info: Optional[dict] = None
    challenge_info: Optional[dict] = None
    clips_creation_entry_point: Optional[str] = None
    content_appreciation_info: Optional[dict] = None
    contextual_highlight_info: Optional[dict] = None
    disable_use_in_clips_client_cache: Optional[bool] = None
    external_media_info: Optional[dict] = None
    featured_label: Optional[str] = None
    is_fan_club_promo_video: Optional[bool] = None
    is_public_chat_welcome_video: Optional[bool] = None
    is_shared_to_fb: Optional[bool] = None
    mashup_info: Optional[MashupInfo] = None
    merchandising_pill_info: Optional[dict] = None
    music_canonical_id: Optional[str | int] = None
    music_info: Optional[MusicInfo] = None
    nux_info: Optional[dict] = None
    original_sound_info: Optional[dict] = None
    professional_clips_upsell_type: Optional[int | str] = None
    reels_on_the_rise_info: Optional[dict] = None
    reusable_text_attribute_string: Optional[str] = None
    reusable_text_info: Optional[list] = None
    shopping_info: Optional[dict] = None
    show_achievements: Optional[bool] = None
    show_tips: Optional[bool | str | list | dict] = None
    template_info: Optional[dict] = None
    viewer_interaction_settings: Optional[dict] = None


class MediaPost(BaseModel, MediaPostItemMixin):
    can_reshare: Optional[bool] = None
    can_save: Optional[bool] = None
    can_see_insights_as_brand: Optional[bool] = None
    can_view_more_preview_comments: Optional[bool] = None
    caption: Optional[MediaPostCaption] = None
    caption_is_edited: Optional[bool] = None
    carousel_media: Optional[list[CarouselItem]] = None
    carousel_media_count: Optional[int] = None
    carousel_media_ids: Optional[list[int]] = None
    carousel_media_pending_post_count: Optional[int] = None
    clips_tab_pinned_user_ids: Optional[list[int]] = None
    code: Optional[str] = None
    comment_count: Optional[int] = None
    comment_inform_treatment: Optional[CommentInformTreatment] = None
    comment_threading_enabled: Optional[bool] = None
    commerciality_status: Optional[str] = None
    deleted_reason: Optional[int | str] = None
    device_timestamp: Optional[int] = None
    explore_hide_comments: Optional[bool] = None
    featured_products: Optional[list] = None
    filter_type: Optional[int] = None
    fundraiser_tag: Optional[FundraiserTag] = None
    has_delayed_metadata: Optional[bool] = None
    has_liked: Optional[bool] = None
    has_more_comments: Optional[bool] = None
    clips_metadata: Optional[ClipsMetadata] = None
    has_shared_to_fb: Optional[int] = None
    hide_view_all_comment_entrypoint: Optional[bool] = None
    id: Optional[int | str] = None
    ig_media_sharing_disabled: Optional[bool] = None
    image_versions: Optional[MediaPostImageVersions] = None
    inline_composer_display_condition: Optional[str] = None
    inline_composer_imp_trigger_time: Optional[int] = None
    integrity_review_decision: Optional[str] = None
    is_auto_created: Optional[bool] = None
    is_comments_gif_composer_enabled: Optional[bool] = None
    is_cutout_sticker_allowed: Optional[bool] = None
    is_in_profile_grid: Optional[bool] = None
    is_open_to_public_submission: Optional[bool] = None
    is_organic_product_tagging_eligible: Optional[bool] = None
    is_paid_partnership: Optional[bool] = None
    is_post_live_clips_media: Optional[bool] = None
    is_quiet_post: Optional[bool] = None
    is_reshare_of_text_post_app_media_in_ig: Optional[bool] = None
    is_unified_video: Optional[bool] = None
    is_visual_reply_commenter_notice_enabled: Optional[bool] = None
    like_and_view_counts_disabled: Optional[bool] = None
    like_count: Optional[int] = None
    play_count: Optional[int] = None
    location: Optional[Location] = None
    mashup_info: Optional[MashupInfo] = None
    max_num_visible_preview_comments: Optional[int] = None
    media_type: Optional[int] = None
    music_metadata: Optional[MusicMetadata] = None
    original_height: Optional[int] = None
    original_media_has_visual_reply_media: Optional[bool] = None
    original_width: Optional[int] = None
    pk: Optional[int | str] = None
    preview_comments: Optional[list] = None
    product_suggestions: Optional[list] = None
    product_type: Optional[str] = None
    profile_grid_control_enabled: Optional[bool] = None
    sharing_friction_info: Optional[SharingFrictionInfo] = None
    shop_routing_user_id: Optional[str | int] = None
    should_request_ads: Optional[bool] = None
    taken_at: Optional[int] = None
    top_likers: Optional[list] = None
    user: Optional[MediaPostUser] = None
    usertags: Optional[dict[str, list[UserTagsInItem]]] = None
    video_codec: Optional[str] = None
    video_duration: Optional[float] = None
    video_versions: Optional[list[VideoVersion]] = None


class MediaPostsChunkItemCaptionText(BaseModel):
    text: Optional[str] = None


class MediaPostsChunkItemCaption(BaseModel):
    items: Optional[list[MediaPostsChunkItemCaptionText]] = None


class CoauthorProducer(BaseModel, UserItemMixin):
    id: Optional[str | int] = None
    is_verified: Optional[bool] = None
    profile_pic_url: Optional[str] = None
    username: Optional[str] = None


class DashInfo(BaseModel):
    is_dash_eligible: Optional[bool] = None
    number_of_qualities: Optional[int] = None


class Dimension(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None


class DisplayVersion(BaseModel):
    config_height: Optional[int] = None
    config_width: Optional[int] = None
    src: Optional[str] = None


class Owner(BaseModel, UserItemMixin):
    id: Optional[str | int] = None
    username: Optional[str] = None


class PinnedUser(BaseModel, UserItemMixin):
    id: Optional[str | int] = None
    is_verified: Optional[bool] = None
    profile_pic_url: Optional[str] = None
    username: Optional[str] = None


class PreviewLikes(BaseModel):
    count: Optional[int] = None
    items: Optional[list] = None


class SponsorUsers(BaseModel):
    item: Optional[list] = None


class TaggedUser(BaseModel, UserItemMixin):
    followed_by_viewer: Optional[bool] = None
    full_name: Optional[str] = None
    id: Optional[str | int] = None
    is_verified: Optional[bool] = None
    profile_pic_url: Optional[str] = None
    username: Optional[str] = None


class TaggedUserInfo(BaseModel):
    user: Optional[TaggedUser] = None
    x: Optional[int | float] = None
    y: Optional[int | float] = None


class TaggedUsers(BaseModel):
    items: Optional[list[TaggedUserInfo]] = None


class ThumbnailVersion(BaseModel):
    config_height: Optional[int] = None
    config_width: Optional[int] = None
    src: Optional[str] = None


class MediaPostsChunkItem(BaseModel, MediaPostItemMixin):
    can_reshare: Optional[bool] = None
    captions: Optional[MediaPostsChunkItemCaption] = None
    coauthor_producers: Optional[list[CoauthorProducer]] = None
    code: Optional[str] = None
    comments: Optional[CountDict] = None
    comments_disabled: Optional[bool] = None
    dash_info: Optional[DashInfo] = None
    dimensions: Optional[Dimension] = None
    display_url: Optional[str] = None
    display_versions: Optional[list[DisplayVersion]] = None
    fact_check_information: Optional[str | int] = None
    fact_check_overall_rating: Optional[int | float] = None
    has_audio: Optional[bool] = None
    has_upcoming_event: Optional[bool] = None
    id: Optional[str | int] = None
    is_affiliate: Optional[bool] = None
    is_paid_partnership: Optional[bool] = None
    is_video: Optional[bool] = None
    location: Optional[Location] = None
    media_overlay_info: Optional[dict] = None
    media_preview: Optional[str] = None
    nft_asset_info: Optional[dict] = None
    owner: Optional[Owner] = None
    pinned_for_users: Optional[list[PinnedUser]] = None
    preview_likes: Optional[PreviewLikes] = None
    product_type: Optional[str] = None
    sensitivity_friction_info: Optional[dict] = None
    sharing_friction_info: Optional[SharingFrictionInfo] = None
    sponsor_users: Optional[SponsorUsers] = None
    tagged_users: Optional[TaggedUsers] = None
    taken_at_timestamp: Optional[int] = None
    thumbnail_src: Optional[str] = None
    thumbnail_versions: Optional[list[ThumbnailVersion]] = None
    type: Optional[str] = None
    video_url: Optional[str] = None
    video_view_count: Optional[int] = None


class MediaPostsData(BaseModel):
    count: Optional[int] = None
    items: Optional[list[MediaPostsChunkItem]] = None
    total: Optional[int] = None


class MediaPostsChunk(BaseModel, NextChunkMixin):
    user_identifier: Optional[str] = None
    data: Optional[MediaPostsData] = None
    pagination_token: Optional[str] = None

    def __init__(self, *args, client, **kwargs):
        self.set_client(client)
        super().__init__(*args, **kwargs)

    def next_chunk(self) -> "MediaPostsChunk":
        """
        This method calls the client.get_user_medias_chunk method.
        See the documentation for this method in the Client or MediaPostMixin class
        """
        self.check_next_chunk()
        client = self.get_client()
        return client.get_user_medias_chunk(
            username_or_id_or_url=self.user_identifier,
            pagination_token=self.pagination_token
        )


class FanClubStatusSyncInfo(BaseModel):
    eligible_to_subscribe: Optional[bool] = None
    subscribed: Optional[bool] = None


class CommentChunkItemCaptionUser(BaseModel, UserItemMixin):
    fan_club_status_sync_info: Optional[FanClubStatusSyncInfo] = None
    fbid_v2: Optional[str | int] = None
    full_name: Optional[str] = None
    id: Optional[str | int] = None
    is_mentionable: Optional[bool] = None
    is_private: Optional[bool] = None
    is_verified: Optional[bool] = None
    profile_pic_id: Optional[str | int] = None
    profile_pic_url: Optional[str] = None
    username: Optional[str] = None


class CommentsChunkItemCaption(BaseModel):
    content_type: Optional[str] = None
    created_at: Optional[int] = None
    created_at_utc: Optional[int] = None
    did_report_as_spam: Optional[bool] = None
    is_covered: Optional[bool] = None
    is_created_by_media_owner: Optional[bool] = None
    is_ranked_comment: Optional[bool] = None
    pk: Optional[str] = None
    share_enabled: Optional[bool] = None
    text: Optional[str] = None
    type: Optional[int | str] = None
    user: Optional[CommentChunkItemCaptionUser] = None
    user_id: Optional[int | str] = None


class QuickEmoji(BaseModel):
    unicode: Optional[str] = None


class CommentsChunkAdditionalData(BaseModel):
    caption: Optional[CommentsChunkItemCaption] = None
    caption_is_edited: Optional[bool] = None
    comment_filter_param: Optional[str] = None
    comment_likes_enabled: Optional[bool] = None
    insert_new_comment_to_top: Optional[bool] = None
    is_ranked: Optional[bool] = None
    media_header_display: Optional[str] = None
    quick_response_emojis: Optional[list[QuickEmoji]] = None
    threading_enabled: Optional[bool] = None


class CommentChunkUser(BaseModel, UserItemMixin):
    fbid_v2: Optional[str | int] = None
    full_name: Optional[str] = None
    id: Optional[str | int] = None
    is_mentionable: Optional[bool] = None
    is_private: Optional[bool] = None
    is_verified: Optional[bool] = None
    latest_besties_reel_media: Optional[int] = None
    latest_reel_media: Optional[int] = None
    profile_pic_url: Optional[str] = None
    username: Optional[str] = None


class CommentsChunkItem(BaseModel):
    child_comment_count: Optional[int] = None
    comment_index: Optional[int] = None
    comment_like_count: Optional[int] = None
    content_type: Optional[str] = None
    created_at: Optional[int] = None
    created_at_utc: Optional[int] = None
    did_report_as_spam: Optional[bool] = None
    has_liked: Optional[bool] = None
    has_liked_comment: Optional[bool] = None
    has_more_head_child_comments: Optional[bool] = None
    has_more_tail_child_comments: Optional[bool] = None
    id: Optional[str | int] = None
    inline_composer_display_condition: Optional[str] = None
    is_covered: Optional[bool] = None
    is_ranked_comment: Optional[bool] = None
    like_count: Optional[int] = None
    other_preview_users: Optional[list[PreviewUser]] = None
    pk: Optional[str | int] = None
    private_reply_status: Optional[int] = None
    share_enabled: Optional[bool] = None
    text: Optional[str] = None
    type: Optional[int | str] = None
    user: Optional[CommentChunkUser] = None
    user_id: Optional[int | str] = None

    def get_comment_thread_chunk(self, client, pagination_token: str = None) -> "CommentsThreadChunk":
        """
        This method calls the client.get_comment_thread_chunk method.
        See the documentation for this method in the Client or MediaPostMixin class
        """
        return client.get_comment_thread_chunk(
            comment_id=self.id,
            pagination_token=pagination_token
        )

    def has_thread_comments(self) -> bool:
        try:
            return self.child_comment_count > 0
        except Exception:
            return False


class CommentsChunkData(BaseModel):
    additional_data: Optional[CommentsChunkAdditionalData] = None
    count: Optional[int] = None
    items: Optional[list[CommentsChunkItem]] = None


class CommentsChunk(BaseModel, NextChunkMixin):
    media_identifier: Optional[str] = None
    data: Optional[CommentsChunkData] = None
    pagination_token: Optional[str] = None

    def __init__(self, *args, client, **kwargs):
        self.set_client(client)
        super().__init__(*args, **kwargs)

    def next_chunk(self) -> "CommentsChunk":
        """
        This method calls the client.get_media_comments_chunk method.
        See the documentation for this method in the Client or MediaPostMixin class
        """
        self.check_next_chunk()
        client = self.get_client()
        return client.get_media_comments_chunk(
            code_or_id_or_url=self.media_identifier,
            pagination_token=self.pagination_token
        )


class CommentsThreadOwner(Owner):
    profile_pic_url: Optional[str] = None


class CommentsThreadChunkItem(BaseModel):
    created_at: Optional[int] = None
    id: Optional[str | int] = None
    is_restricted_pending: Optional[bool] = None
    liked_by: Optional[CountDict] = None
    owner: Optional[CommentsThreadOwner] = None
    text: Optional[str] = None


class CommentsThreadChunkData(BaseModel):
    count: Optional[int] = None
    items: Optional[list[CommentsThreadChunkItem]] = None


class CommentsThreadChunk(BaseModel, NextChunkMixin):
    commend_id: Optional[str | int] = None
    data: Optional[CommentsThreadChunkData] = None
    pagination_token: Optional[str] = None

    def __init__(self, *args, client, **kwargs):
        self.set_client(client)
        super().__init__(*args, **kwargs)

    def next_chunk(self) -> "CommentsThreadChunk":
        """
        This method calls the client.get_comment_thread_chunk method.
        See the documentation for this method in the Client or MediaPostMixin class
        """
        self.check_next_chunk()
        client = self.get_client()
        return client.get_comment_thread_chunk(
            comment_id=self.commend_id,
            pagination_token=self.pagination_token
        )


class SimilarAccounts(BaseModel):
    count: Optional[int] = None
    items: Optional[list[ShortUser]] = None


class MediaPostsHashtagChunkAdditionalData(BaseModel):
    allow_following: Optional[int] = None
    allow_muting_story: Optional[bool] = None
    content_advisory: Optional[str | list | dict] = None
    follow_button_text: Optional[str] = None
    formatted_media_count: Optional[str] = None
    fresh_topic_metadata: Optional[dict] = None
    hide_use_hashtag_button: Optional[bool] = None
    id: Optional[int | str] = None
    is_trending: Optional[bool] = None
    media_count: Optional[int] = None
    name: Optional[str] = None
    non_violating: Optional[int] = None
    profile_pic_url: Optional[str] = None
    promo_banner: Optional[str | dict] = None
    related_tags: Optional[list | dict] = None
    show_follow_drop_down: Optional[bool] = None
    social_context: Optional[str] = None
    social_context_profile_links: Optional[list] = None
    subtitle: Optional[str] = None
    warning_message: Optional[str] = None


class HashtagMediaPostImageVersionsItem(BaseModel):
    height: Optional[int] = None
    scans_profile: Optional[str] = None
    url: Optional[str] = None
    width: Optional[int] = None


class HashtagMediaPostImageVersions(BaseModel):
    additional_items: Optional[dict] = None
    items: Optional[list[HashtagMediaPostImageVersionsItem]] = None
    scrubber_spritesheet_info_candidates: Optional[dict] = None
    smart_thumbnail_enabled: Optional[bool] = None


class MediaAppreciationSettings(BaseModel):
    gift_count_visibility: Optional[str] = None
    media_gifting_state: Optional[str] = None


class SquareCrop(BaseModel):
    crop_bottom: Optional[int | float] = None
    crop_left: Optional[int | float] = None
    crop_right: Optional[int | float] = None
    crop_top: Optional[int | float] = None


class MediaCroppingInfo(BaseModel):
    square_crop: Optional[SquareCrop] = None


class HashtagMediaPost(MediaPost):
    clips_metadata: Optional[ClipsMetadata] = None
    enable_waist: Optional[bool] = None
    feed_type: Optional[str] = None
    has_audio: Optional[bool] = None
    image_versions: Optional[HashtagMediaPostImageVersions] = None
    inventory_source: Optional[str] = None
    is_artist_pick: Optional[bool] = None
    is_dash_eligible: Optional[int] = None
    is_third_party_downloads_eligible: Optional[bool] = None
    lat: Optional[float] = None
    layout_type: Optional[str] = None
    lng: Optional[float] = None
    location: Optional[Location] = None
    media_appreciation_settings: Optional[MediaAppreciationSettings] = None
    media_cropping_info: Optional[MediaCroppingInfo] = None
    number_of_qualities: Optional[int] = None
    play_count: Optional[int] = None
    reshare_count: Optional[int] = None
    social_context: Optional[list] = None
    video_codec: Optional[str] = None
    video_duration: Optional[float] = None
    video_versions: Optional[list[VideoVersion]] = None
    view_state_item_type: Optional[int] = None


class MediaPostsHashtagChunkData(BaseModel):
    additional_data: Optional[MediaPostsHashtagChunkAdditionalData] = None
    count: Optional[int] = None
    items: Optional[list[HashtagMediaPost]] = None


class MediaPostsHashtagChunk(BaseModel, NextChunkMixin):
    hashtag: Optional[str] = None
    data: Optional[MediaPostsHashtagChunkData] = None
    pagination_token: Optional[str] = None

    def __init__(self, *args, client, **kwargs):
        self.set_client(client)
        super().__init__(*args, **kwargs)

    def next_chunk(self) -> "MediaPostsHashtagChunk":
        """
        This method calls the client.get_medias_by_hashtag_chunk method.
        See the documentation for this method in the Client or MediaPostMixin class
        """
        self.check_next_chunk()
        client = self.get_client()
        return client.get_medias_by_hashtag_chunk(
            hashtag=self.hashtag,
            pagination_token=self.pagination_token
        )


class TaggedMediaPostCaptionItem(BaseModel):
    text: Optional[str] = None


class TaggedMediaPostCaption(BaseModel):
    items: Optional[list[TaggedMediaPostCaptionItem]] = None


class TaggedMediaPost(BaseModel, MediaPostItemMixin):
    accessibility_caption: Optional[str] = None
    captions: Optional[TaggedMediaPostCaption] = None
    code: Optional[str] = None
    comments: Optional[CountDict] = None
    comments_disabled: Optional[bool] = None
    dimensions: Optional[Dimension] = None
    display_url: Optional[str] = None
    has_upcoming_event: Optional[bool] = None
    id: Optional[str | int] = None
    is_video: Optional[bool] = None
    liked_by: Optional[CountDict] = None
    owner: Optional[Owner] = None
    preview_likes: Optional[CountDict] = None
    taken_at_timestamp: Optional[int] = None
    thumbnail_src: Optional[str] = None
    type: Optional[str] = None


class TaggedMediaPostsChunkData(CountDict):
    items: Optional[list[TaggedMediaPost]] = None


class TaggedMediaPostsChunk(BaseModel, NextChunkMixin):
    user_identifier: Optional[str] = None
    data: Optional[TaggedMediaPostsChunkData] = None
    pagination_token: Optional[str] = None

    def __init__(self, *args, client, **kwargs):
        self.set_client(client)
        super().__init__(*args, **kwargs)

    def next_chunk(self) -> "TaggedMediaPostsChunk":
        """
        This method calls the client.get_tagged_medias_chunk method.
        See the documentation for this method in the Client or MediaPostMixin class
        """
        self.check_next_chunk()
        client = self.get_client()
        return client.get_tagged_medias_chunk(
            username_or_id_or_url=self.user_identifier,
            pagination_token=self.pagination_token
        )


class SearchHashtag(BaseModel):
    id: Optional[int] = None
    media_count: Optional[int] = None
    name: Optional[str] = None
    position: Optional[int] = None
    search_result_subtitle: Optional[str] = None
    use_default_avatar: Optional[bool] = None


class SearchPlace(BaseModel):
    location: Optional[Location] = None
    media_bundles: Optional[list] = None
    position: Optional[int] = None
    slug: Optional[str] = None
    subtitle: Optional[str] = None
    title: Optional[str] = None


class SearchUser(BaseModel, UserItemMixin):
    account_badges: Optional[list] = None
    birthday_today_visibility_for_viewer: Optional[str] = None
    fbid_v2: Optional[int | str] = None
    full_name: Optional[str] = None
    has_anonymous_profile_picture: Optional[bool] = None
    has_opt_eligible_shop: Optional[bool] = None
    id: Optional[str | int] = None
    is_private: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_verified_search_boosted: Optional[bool] = None
    latest_reel_media: Optional[int] = None
    position: Optional[int] = None
    profile_pic_id: Optional[str | int] = None
    profile_pic_url: Optional[str] = None
    search_social_context: Optional[str] = None
    should_show_category: Optional[bool] = None
    show_ig_app_switcher_badge: Optional[bool] = None
    show_text_post_app_badge: Optional[bool] = None
    social_context: Optional[str] = None
    third_party_downloads_enabled: Optional[int] = None
    username: Optional[str] = None


class SearchResult(BaseModel):
    hashtags: Optional[list[SearchHashtag]] = None
    places: Optional[list[SearchPlace]] = None
    rank_token: Optional[str | float] = None
    users: Optional[list[SearchUser]] = None
