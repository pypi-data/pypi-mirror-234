use crate::bounded::Bounded;
use crate::operations::{
    to_boxes_ids_with_intersection, IntersectCrossingSegments, Orient,
};
use crate::relatable::{Relatable, Relation};
use crate::sweeping::traits::{EventsQueue, SweepLine};
use crate::traits::{
    Contoural, Elemental, Iterable, Lengthsome, Multipolygonal,
    MultipolygonalIntoIteratorPolygon, Multisegmental,
    MultisegmentalIndexSegment, MultivertexalIndexVertex, Polygonal,
    PolygonalContour, PolygonalIndexHole, PolygonalIntoIteratorHole,
    Segmental,
};

use super::event::Event;
use super::{mixed, shaped};

pub(crate) fn relate_to_contour<
    Contour,
    Multipolygon,
    Point: Clone + Ord,
    Polygon,
    Scalar: Ord,
    Segment: Clone + Segmental<Endpoint = Point>,
>(
    multipolygon: &Multipolygon,
    contour: &Contour,
) -> Relation
where
    mixed::Operation<false, Point>:
        EventsQueue<Event = Event> + SweepLine<Event = Event>,
    for<'a> &'a Contour: Bounded<&'a Scalar>
        + Contoural<IndexSegment = Segment, IntoIteratorSegment = &'a Segment>,
    for<'a> &'a Multipolygon:
        Bounded<&'a Scalar> + Multipolygonal<IndexPolygon = Polygon>,
    for<'a> &'a Point: Elemental<Coordinate = &'a Scalar>
        + IntersectCrossingSegments<Output = Point>
        + Orient,
    for<'a> &'a Polygon: Bounded<&'a Scalar>
        + Polygonal<Contour = &'a Contour, IntoIteratorHole = &'a Contour>,
    for<'a> &'a Segment: Bounded<&'a Scalar> + Segmental<Endpoint = &'a Point>,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Segmental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Elemental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b> &'a MultivertexalIndexVertex<&'b Contour>: Elemental,
    for<'a, 'b> &'a PolygonalIndexHole<
        MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
    >: Contoural,
    for<'a, 'b> &'a PolygonalIndexHole<&'b Polygon>: Contoural,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<&'b PolygonalIndexHole<&'c Polygon>>:
        Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<&'b PolygonalIndexHole<&'c Polygon>>:
        Elemental,
{
    relate_to_multisegmental::<
        false,
        Contour,
        Multipolygon,
        Contour,
        Point,
        Polygon,
        Scalar,
        Segment,
    >(multipolygon, contour)
}

pub(crate) fn relate_to_multipolygon<
    Border,
    Multipolygon,
    Point: Clone + Ord,
    Polygon,
    Scalar: Ord,
    Segment: Clone + Segmental<Endpoint = Point>,
>(
    first: &Multipolygon,
    second: &Multipolygon,
) -> Relation
where
    shaped::Operation<Point>:
        EventsQueue<Event = Event> + SweepLine<Event = Event>,
    for<'a> &'a Border:
        Bounded<&'a Scalar> + Contoural<IntoIteratorSegment = &'a Segment>,
    for<'a> &'a Multipolygon:
        Bounded<&'a Scalar> + Multipolygonal<IndexPolygon = Polygon>,
    for<'a> &'a Point: Elemental<Coordinate = &'a Scalar>
        + IntersectCrossingSegments<Output = Point>
        + Orient,
    for<'a> &'a Polygon: Bounded<&'a Scalar>
        + Polygonal<Contour = &'a Border, IntoIteratorHole = &'a Border>,
    for<'a> &'a Segment: Bounded<&'a Scalar> + Segmental<Endpoint = &'a Point>,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Segmental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Elemental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<&'b Border>: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<&'b Border>: Elemental,
    for<'a, 'b> &'a PolygonalIndexHole<
        MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
    >: Contoural,
    for<'a, 'b> &'a PolygonalIndexHole<&'b Polygon>: Contoural,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<&'b PolygonalIndexHole<&'c Polygon>>:
        Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<&'b PolygonalIndexHole<&'c Polygon>>:
        Elemental,
{
    let first_bounding_box = first.to_bounding_box();
    let second_bounding_box = second.to_bounding_box();
    if first_bounding_box.disjoint_with(&second_bounding_box) {
        return Relation::Disjoint;
    }
    let first_polygons = first.polygons();
    let first_bounding_boxes = first_polygons
        .iter()
        .map(Bounded::to_bounding_box)
        .collect::<Vec<_>>();
    let first_intersecting_polygons_ids = to_boxes_ids_with_intersection(
        &first_bounding_boxes,
        &second_bounding_box,
    );
    if first_intersecting_polygons_ids.is_empty() {
        return Relation::Disjoint;
    }
    let second_polygons = second.polygons();
    let second_bounding_boxes = second_polygons
        .iter()
        .map(Bounded::to_bounding_box)
        .collect::<Vec<_>>();
    let second_intersecting_polygons_ids = to_boxes_ids_with_intersection(
        &second_bounding_boxes,
        &first_bounding_box,
    );
    let min_max_x = unsafe {
        first_intersecting_polygons_ids
            .iter()
            .map(|&index| first_bounding_boxes[index].get_max_x())
            .max()
            .unwrap_unchecked()
    }
    .min(unsafe {
        second_intersecting_polygons_ids
            .iter()
            .map(|&index| second_bounding_boxes[index].get_max_x())
            .max()
            .unwrap_unchecked()
    });
    let first_intersecting_polygons_borders_segments =
        first_intersecting_polygons_ids
            .iter()
            .map(|&polygon_id| first_polygons[polygon_id].border().segments())
            .collect::<Vec<_>>();
    let first_intersecting_polygons_holes_segments =
        first_intersecting_polygons_ids
            .iter()
            .flat_map(|&polygon_id| {
                first_polygons[polygon_id].holes().into_iter().filter_map(
                    |hole| {
                        if hole
                            .to_bounding_box()
                            .disjoint_with(&second_bounding_box)
                        {
                            None
                        } else {
                            Some(hole.segments())
                        }
                    },
                )
            })
            .collect::<Vec<_>>();
    let second_intersecting_polygons_borders_segments =
        second_intersecting_polygons_ids
            .iter()
            .map(|&polygon_id| second_polygons[polygon_id].border().segments())
            .collect::<Vec<_>>();
    let second_intersecting_polygons_holes_segments =
        second_intersecting_polygons_ids
            .iter()
            .flat_map(|&polygon_id| {
                second_polygons[polygon_id].holes().into_iter().filter_map(
                    |hole| {
                        if hole
                            .to_bounding_box()
                            .disjoint_with(&second_bounding_box)
                        {
                            None
                        } else {
                            Some(hole.segments())
                        }
                    },
                )
            })
            .collect::<Vec<_>>();
    shaped::Operation::<Point>::from_segments_iterators(
        (
            first_intersecting_polygons_borders_segments
                .iter()
                .map(|segments| segments.len())
                .sum::<usize>()
                + first_intersecting_polygons_holes_segments
                    .iter()
                    .map(|segments| segments.len())
                    .sum::<usize>(),
            first_intersecting_polygons_borders_segments
                .into_iter()
                .flat_map(|border_segments| {
                    border_segments.into_iter().cloned()
                })
                .chain(
                    first_intersecting_polygons_holes_segments
                        .into_iter()
                        .flat_map(|hole_segments| {
                            hole_segments.into_iter().cloned()
                        }),
                ),
        ),
        (
            second_intersecting_polygons_borders_segments
                .iter()
                .map(|segments| segments.len())
                .sum::<usize>()
                + second_intersecting_polygons_holes_segments
                    .iter()
                    .map(|segments| segments.len())
                    .sum::<usize>(),
            second_intersecting_polygons_borders_segments
                .into_iter()
                .flat_map(|border_segments| {
                    border_segments.into_iter().cloned()
                })
                .chain(
                    second_intersecting_polygons_holes_segments
                        .into_iter()
                        .flat_map(|hole_segments| {
                            hole_segments.into_iter().cloned()
                        }),
                ),
        ),
    )
    .into_relation(
        first_intersecting_polygons_ids.len() == first_polygons.len(),
        second_intersecting_polygons_ids.len() == second_polygons.len(),
        min_max_x,
    )
}

pub(crate) fn relate_to_multisegment<
    Border,
    Multipolygon,
    Multisegment,
    Point: Clone + Ord,
    Polygon,
    Scalar: Ord,
    Segment: Clone + Segmental<Endpoint = Point>,
>(
    multipolygon: &Multipolygon,
    multisegment: &Multisegment,
) -> Relation
where
    mixed::Operation<false, Point>:
        EventsQueue<Event = Event> + SweepLine<Event = Event>,
    for<'a> &'a Border:
        Bounded<&'a Scalar> + Contoural<IntoIteratorSegment = &'a Segment>,
    for<'a> &'a Multipolygon:
        Bounded<&'a Scalar> + Multipolygonal<IndexPolygon = Polygon>,
    for<'a> &'a Multisegment:
        Bounded<&'a Scalar> + Multisegmental<IndexSegment = Segment>,
    for<'a> &'a Point: Elemental<Coordinate = &'a Scalar>
        + IntersectCrossingSegments<Output = Point>
        + Orient,
    for<'a> &'a Polygon: Bounded<&'a Scalar>
        + Polygonal<Contour = &'a Border, IntoIteratorHole = &'a Border>,
    for<'a> &'a Segment: Bounded<&'a Scalar> + Segmental<Endpoint = &'a Point>,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Segmental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Elemental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<&'b Border>: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<&'b Border>: Elemental,
    for<'a, 'b> &'a PolygonalIndexHole<
        MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
    >: Contoural,
    for<'a, 'b> &'a PolygonalIndexHole<&'b Polygon>: Contoural,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<&'b PolygonalIndexHole<&'c Polygon>>:
        Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<&'b PolygonalIndexHole<&'c Polygon>>:
        Elemental,
{
    relate_to_multisegmental::<
        false,
        Border,
        Multipolygon,
        Multisegment,
        Point,
        Polygon,
        Scalar,
        Segment,
    >(multipolygon, multisegment)
}

pub(crate) fn relate_to_polygon<
    Border,
    Multipolygon,
    Point: Clone + Ord,
    Polygon,
    Scalar: Ord,
    Segment: Clone + Segmental<Endpoint = Point>,
>(
    multipolygonal: &Multipolygon,
    polygon: &Polygon,
) -> Relation
where
    shaped::Operation<Point>:
        EventsQueue<Event = Event> + SweepLine<Event = Event>,
    for<'a> &'a Border:
        Bounded<&'a Scalar> + Contoural<IntoIteratorSegment = &'a Segment>,
    for<'a> &'a Multipolygon:
        Bounded<&'a Scalar> + Multipolygonal<IndexPolygon = Polygon>,
    for<'a> &'a Point: Elemental<Coordinate = &'a Scalar>
        + IntersectCrossingSegments<Output = Point>
        + Orient,
    for<'a> &'a Polygon: Bounded<&'a Scalar>
        + Polygonal<Contour = &'a Border, IntoIteratorHole = &'a Border>,
    for<'a> &'a Segment: Bounded<&'a Scalar> + Segmental<Endpoint = &'a Point>,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Segmental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Elemental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<&'b Border>: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<&'b Border>: Elemental,
    for<'a, 'b> &'a PolygonalIndexHole<
        MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
    >: Contoural,
    for<'a, 'b> &'a PolygonalIndexHole<&'b Polygon>: Contoural,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<&'b PolygonalIndexHole<&'c Polygon>>:
        Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<&'b PolygonalIndexHole<&'c Polygon>>:
        Elemental,
{
    let multipolygonal_bounding_box = multipolygonal.to_bounding_box();
    let polygon_bounding_box = polygon.to_bounding_box();
    if multipolygonal_bounding_box.disjoint_with(&polygon_bounding_box) {
        return Relation::Disjoint;
    }
    let multipolygonal_polygons = multipolygonal.polygons();
    let multipolygonal_bounding_boxes = multipolygonal_polygons
        .iter()
        .map(Bounded::to_bounding_box)
        .collect::<Vec<_>>();
    let intersecting_polygons_ids = to_boxes_ids_with_intersection(
        &multipolygonal_bounding_boxes,
        &polygon_bounding_box,
    );
    if intersecting_polygons_ids.is_empty() {
        return Relation::Disjoint;
    }
    let min_max_x = unsafe {
        intersecting_polygons_ids
            .iter()
            .map(|&index| multipolygonal_bounding_boxes[index].get_max_x())
            .max()
            .unwrap_unchecked()
    }
    .min(polygon_bounding_box.get_max_x());
    let border_segments = polygon.border().segments();
    let intersecting_holes_segments = polygon
        .holes()
        .into_iter()
        .filter_map(|hole| {
            if hole
                .to_bounding_box()
                .disjoint_with(&multipolygonal_bounding_box)
            {
                None
            } else {
                Some(hole.segments())
            }
        })
        .collect::<Vec<_>>();
    let intersecting_polygons_borders_segments = intersecting_polygons_ids
        .iter()
        .map(|&polygon_id| {
            multipolygonal_polygons[polygon_id].border().segments()
        })
        .collect::<Vec<_>>();
    let intersecting_polygons_holes_segments = intersecting_polygons_ids
        .iter()
        .flat_map(|&polygon_id| {
            multipolygonal_polygons[polygon_id]
                .holes()
                .into_iter()
                .filter_map(|hole| {
                    if hole
                        .to_bounding_box()
                        .disjoint_with(&polygon_bounding_box)
                    {
                        None
                    } else {
                        Some(hole.segments())
                    }
                })
        })
        .collect::<Vec<_>>();
    shaped::Operation::<Point>::from_segments_iterators(
        (
            intersecting_polygons_borders_segments
                .iter()
                .map(|segments| segments.len())
                .sum::<usize>()
                + intersecting_polygons_holes_segments
                    .iter()
                    .map(|segments| segments.len())
                    .sum::<usize>(),
            intersecting_polygons_borders_segments
                .into_iter()
                .flat_map(|border_segments| {
                    border_segments.into_iter().cloned()
                })
                .chain(
                    intersecting_polygons_holes_segments.into_iter().flat_map(
                        |hole_segments| hole_segments.into_iter().cloned(),
                    ),
                ),
        ),
        (
            border_segments.len()
                + intersecting_holes_segments
                    .iter()
                    .map(|hole_segments| hole_segments.len())
                    .sum::<usize>(),
            border_segments.into_iter().cloned().chain(
                intersecting_holes_segments.into_iter().flat_map(
                    |hole_segments| hole_segments.into_iter().cloned(),
                ),
            ),
        ),
    )
    .into_relation(
        intersecting_polygons_ids.len() == multipolygonal_polygons.len(),
        true,
        min_max_x,
    )
}

pub(crate) fn relate_to_segment<
    Border,
    Multipolygon,
    Point: Clone + Ord,
    Polygon,
    Scalar: Ord,
    Segment: Clone + Segmental<Endpoint = Point>,
>(
    multipolygon: &Multipolygon,
    segment: &Segment,
) -> Relation
where
    mixed::Operation<false, Point>:
        EventsQueue<Event = Event> + SweepLine<Event = Event>,
    for<'a> &'a Border:
        Bounded<&'a Scalar> + Contoural<IntoIteratorSegment = &'a Segment>,
    for<'a> &'a Multipolygon: Multipolygonal<IndexPolygon = Polygon>,
    for<'a> &'a Point: Elemental<Coordinate = &'a Scalar>
        + IntersectCrossingSegments<Output = Point>
        + Orient,
    for<'a> &'a Polygon: Bounded<&'a Scalar>
        + Polygonal<Contour = &'a Border, IntoIteratorHole = &'a Border>,
    for<'a> &'a Segment: Bounded<&'a Scalar> + Segmental<Endpoint = &'a Point>,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Segmental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Elemental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<&'b Border>: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<&'b Border>: Elemental,
    for<'a, 'b> &'a PolygonalIndexHole<
        MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
    >: Contoural,
    for<'a, 'b> &'a PolygonalIndexHole<&'b Polygon>: Contoural,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<&'b PolygonalIndexHole<&'c Polygon>>:
        Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<&'b PolygonalIndexHole<&'c Polygon>>:
        Elemental,
{
    let segment_bounding_box = segment.to_bounding_box();
    let polygons = multipolygon.polygons();
    let polygons_bounding_boxes = polygons
        .iter()
        .map(Bounded::to_bounding_box)
        .collect::<Vec<_>>();
    let intersecting_polygons_ids = to_boxes_ids_with_intersection(
        &polygons_bounding_boxes,
        &segment_bounding_box,
    );
    if intersecting_polygons_ids.is_empty() {
        Relation::Disjoint
    } else {
        let min_max_x = segment_bounding_box.get_max_x().min(unsafe {
            intersecting_polygons_ids
                .iter()
                .map(|&border_id| {
                    polygons_bounding_boxes[border_id].get_max_x()
                })
                .max()
                .unwrap_unchecked()
        });
        let intersecting_polygons_borders_segments = intersecting_polygons_ids
            .iter()
            .map(|&polygon_id| polygons[polygon_id].border().segments())
            .collect::<Vec<_>>();
        let intersecting_polygons_holes_segments = intersecting_polygons_ids
            .iter()
            .flat_map(|&polygon_id| {
                polygons[polygon_id].holes().into_iter().filter_map(|hole| {
                    if hole
                        .to_bounding_box()
                        .disjoint_with(&segment_bounding_box)
                    {
                        None
                    } else {
                        Some(hole.segments())
                    }
                })
            })
            .collect::<Vec<_>>();
        mixed::Operation::<false, Point>::from_segments_iterators(
            (
                intersecting_polygons_borders_segments
                    .iter()
                    .map(|segments| segments.len())
                    .sum::<usize>()
                    + intersecting_polygons_holes_segments
                        .iter()
                        .map(|segments| segments.len())
                        .sum::<usize>(),
                intersecting_polygons_borders_segments
                    .into_iter()
                    .flat_map(|border_segments| {
                        border_segments.into_iter().cloned()
                    })
                    .chain(
                        intersecting_polygons_holes_segments
                            .into_iter()
                            .flat_map(|hole_segments| {
                                hole_segments.into_iter().cloned()
                            }),
                    ),
            ),
            (1, std::iter::once(segment.clone())),
        )
        .into_relation(true, min_max_x)
    }
}

fn relate_to_multisegmental<
    const IS_CONTOUR: bool,
    Border,
    Multipolygon,
    Multisegment,
    Point: Clone + Ord,
    Polygon,
    Scalar: Ord,
    Segment: Clone + Segmental<Endpoint = Point>,
>(
    multipolygon: &Multipolygon,
    multisegmental: &Multisegment,
) -> Relation
where
    mixed::Operation<false, Point>:
        EventsQueue<Event = Event> + SweepLine<Event = Event>,
    for<'a> &'a Border:
        Bounded<&'a Scalar> + Contoural<IntoIteratorSegment = &'a Segment>,
    for<'a> &'a Multipolygon:
        Bounded<&'a Scalar> + Multipolygonal<IndexPolygon = Polygon>,
    for<'a> &'a Multisegment:
        Bounded<&'a Scalar> + Multisegmental<IndexSegment = Segment>,
    for<'a> &'a Point: Elemental<Coordinate = &'a Scalar>
        + IntersectCrossingSegments<Output = Point>
        + Orient,
    for<'a> &'a Polygon: Bounded<&'a Scalar>
        + Polygonal<Contour = &'a Border, IntoIteratorHole = &'a Border>,
    for<'a> &'a Segment: Bounded<&'a Scalar> + Segmental<Endpoint = &'a Point>,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Segmental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalContour<MultipolygonalIntoIteratorPolygon<&'b Multipolygon>>,
    >: Elemental,
    for<'a, 'b> &'a MultivertexalIndexVertex<
        PolygonalIntoIteratorHole<
            MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b> &'a MultisegmentalIndexSegment<&'b Border>: Segmental,
    for<'a, 'b> &'a MultivertexalIndexVertex<&'b Border>: Elemental,
    for<'a, 'b> &'a PolygonalIndexHole<
        MultipolygonalIntoIteratorPolygon<&'b Multipolygon>,
    >: Contoural,
    for<'a, 'b> &'a PolygonalIndexHole<&'b Polygon>: Contoural,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<
        &'b PolygonalIndexHole<
            MultipolygonalIntoIteratorPolygon<&'c Multipolygon>,
        >,
    >: Elemental,
    for<'a, 'b, 'c> &'a MultisegmentalIndexSegment<&'b PolygonalIndexHole<&'c Polygon>>:
        Segmental,
    for<'a, 'b, 'c> &'a MultivertexalIndexVertex<&'b PolygonalIndexHole<&'c Polygon>>:
        Elemental,
{
    let multipolygon_bounding_box = multipolygon.to_bounding_box();
    let multisegmental_bounding_box = multisegmental.to_bounding_box();
    if multisegmental_bounding_box.disjoint_with(&multipolygon_bounding_box) {
        return Relation::Disjoint;
    }
    let multisegmental_segments = multisegmental.segments();
    let multisegmental_bounding_boxes = multisegmental_segments
        .iter()
        .map(Bounded::to_bounding_box)
        .collect::<Vec<_>>();
    let intersecting_segments_ids = to_boxes_ids_with_intersection(
        &multisegmental_bounding_boxes,
        &multipolygon_bounding_box,
    );
    if intersecting_segments_ids.is_empty() {
        return Relation::Disjoint;
    } else if intersecting_segments_ids.len() == 1 {
        return match relate_to_segment(
            multipolygon,
            &multisegmental_segments[intersecting_segments_ids[0]],
        ) {
            Relation::Component => Relation::Touch,
            Relation::Enclosed | Relation::Within => Relation::Cross,
            relation => relation,
        };
    }
    let polygons = multipolygon.polygons();
    let polygons_bounding_boxes = polygons
        .iter()
        .map(Bounded::to_bounding_box)
        .collect::<Vec<_>>();
    let intersecting_polygons_ids = to_boxes_ids_with_intersection(
        &polygons_bounding_boxes,
        &multisegmental_bounding_box,
    );
    if intersecting_polygons_ids.is_empty() {
        Relation::Disjoint
    } else {
        let min_max_x = multisegmental_bounding_box.get_max_x().min(unsafe {
            intersecting_polygons_ids
                .iter()
                .map(|&border_id| {
                    polygons_bounding_boxes[border_id].get_max_x()
                })
                .max()
                .unwrap_unchecked()
        });
        let intersecting_polygons_borders_segments = intersecting_polygons_ids
            .iter()
            .map(|&polygon_id| polygons[polygon_id].border().segments())
            .collect::<Vec<_>>();
        let intersecting_polygons_holes_segments = intersecting_polygons_ids
            .iter()
            .flat_map(|&polygon_id| {
                polygons[polygon_id].holes().into_iter().filter_map(|hole| {
                    if hole
                        .to_bounding_box()
                        .disjoint_with(&multisegmental_bounding_box)
                    {
                        None
                    } else {
                        Some(hole.segments())
                    }
                })
            })
            .collect::<Vec<_>>();
        mixed::Operation::<false, Point>::from_segments_iterators(
            (
                intersecting_polygons_borders_segments
                    .iter()
                    .map(|segments| segments.len())
                    .sum::<usize>()
                    + intersecting_polygons_holes_segments
                        .iter()
                        .map(|segments| segments.len())
                        .sum::<usize>(),
                intersecting_polygons_borders_segments
                    .into_iter()
                    .flat_map(|border_segments| {
                        border_segments.into_iter().cloned()
                    })
                    .chain(
                        intersecting_polygons_holes_segments
                            .into_iter()
                            .flat_map(|hole_segments| {
                                hole_segments.into_iter().cloned()
                            }),
                    ),
            ),
            (
                intersecting_segments_ids.len(),
                intersecting_segments_ids
                    .iter()
                    .map(|&index| &multisegmental_segments[index])
                    .cloned(),
            ),
        )
        .into_relation(
            intersecting_segments_ids.len() == multisegmental_segments.len(),
            min_max_x,
        )
    }
}
