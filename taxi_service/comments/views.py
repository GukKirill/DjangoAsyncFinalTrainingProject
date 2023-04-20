from asgiref.sync import sync_to_async, async_to_sync
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import Comment
from trips.models import Trip
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


async def get_comment_data(pk):
    trip = None
    client = None
    u_comment = None
    comment_pk = None
    form = CommentForm()
    async for tr in Trip.objects.filter(pk=pk).select_related('client', 'comment'):
        trip = tr
        client = tr.client
        try:
            u_comment = tr.comment
            comment_pk = u_comment.pk
        except ObjectDoesNotExist:
            pass
    return trip, client, u_comment, comment_pk, form


async def save_comment_data(request, trip, comment_pk, msg, update=False):
    form = CommentForm(request.POST)
    if form.is_valid():
        if not update:
            comment_obj = Comment(
                author=request.user,
                about_driver=form.cleaned_data['about_driver'],
                about_car=form.cleaned_data['about_car'],
                trip=trip
            )
            await sync_to_async(comment_obj.save)()
        else:
            comment_obj = Comment(
                pk=comment_pk,
                about_driver=form.cleaned_data['about_driver'],
                about_car=form.cleaned_data['about_car']
            )
            await sync_to_async(comment_obj.save)(update_fields=['about_driver', 'about_car'])
        await sync_to_async(messages.success)(request, msg)


@sync_to_async
@login_required
@async_to_sync
async def comment(request, pk):
    trip, client, u_comment, comment_pk, form = await get_comment_data(pk)

    if request.user == client:
        if not u_comment:
            if request.method == 'POST':
                await save_comment_data(request, trip, comment_pk, msg=f'Comment created for {trip}')
                return await sync_to_async(redirect)('home')
        else:
            await sync_to_async(messages.success)(
                request, """Client can't comment this trip again. Choose "update" or "delete" functions"""
            )
            return await sync_to_async(redirect)('home')
    else:
        await sync_to_async(messages.success)(request, 'Wrong client for this trip')
        return await sync_to_async(redirect)('home')

    context = {
        'pk': pk,
        'form': form,
        'trip': trip,
        'comment': u_comment,
    }
    return await sync_to_async(render)(request, 'comment.html', context=context)


@sync_to_async
@login_required
@async_to_sync
async def comment_update(request, pk):
    trip, client, u_comment, comment_pk, form = await get_comment_data(pk)
    if request.user == client:
        if u_comment:
            if request.method == 'POST':
                await save_comment_data(request, trip, comment_pk, msg=f'Comment updated for {trip}', update=True)
                return await sync_to_async(redirect)('home')
        else:
            await sync_to_async(messages.success)(
                request, """Client can't update this comment. Choose "create" function"""
            )
            return await sync_to_async(redirect)('home')
    else:
        await sync_to_async(messages.success)(request, 'Wrong client for this trip')
        return await sync_to_async(redirect)('home')

    form.fields['about_driver'].initial = u_comment.about_driver
    form.fields['about_car'].initial = u_comment.about_car
    context = {
        'pk': pk,
        'form': form,
        'trip': trip,
        'comment': u_comment,
    }
    return await sync_to_async(render)(request, 'update_comment.html', context=context)


@sync_to_async
@login_required
@async_to_sync
async def comment_delete(request, pk):
    u_comment = None
    async for element in Comment.objects.filter(pk=pk).select_related('author'):
        u_comment = element
    if request.user == u_comment.author:
        if u_comment:
            if request.method == 'POST':
                await sync_to_async(u_comment.delete)()
                await sync_to_async(messages.success)(request, 'Comment deleted')
                return await sync_to_async(redirect)('home')
        else:
            await sync_to_async(messages.success)(request, 'No comments for this trip')
            return await sync_to_async(redirect)('home')
    else:
        await sync_to_async(messages.success)(request, 'Wrong client for this trip')
        return await sync_to_async(redirect)('home')
    context = {
        'comment': u_comment,
    }
    return await sync_to_async(render)(request, 'delete_comment.html', context=context)
