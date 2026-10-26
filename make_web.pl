#!/usr/bin/perl
# 게시용 만들기 — 강의용 docs/261026.html 의 로컬 영상을 유튜브로 바꿔 docs/261026-web.html 로 쓴다
# (대표 10-26 «게시용은 유툽에 영상올려서 처리하자» · 강의용은 로컬 영상 그대로)
#   영상 → 유튜브 짝은 youtube-links.tsv (까치 10-26 08:51 업로드)
#   짝이 없는 영상은 «추후 업로드» 자리로 둔다 — 2-3 TAKE2·3 (대표 «추후업로드할예정»)
#   작업물 예시 PDF 는 저장소 밖이라 게시용에서 뺀다
# 쓰는 법: quarto 로 261026.html 을 만든 뒤  perl make_web.pl
use strict; use warnings; use utf8;
use Encode qw(decode_utf8 encode_utf8);
use Unicode::Normalize qw(NFC);
binmode STDOUT, ':utf8';

my $in  = 'docs/261026.html';
my $out = 'docs/261026-web.html';
my $dir = '에이전틱코딩촬영영상/';

my %yt;
open my $t, '<:utf8', 'youtube-links.tsv' or die "youtube-links.tsv: $!";
while (<$t>) { next if /^#/; chomp; my ($p, $id) = split /\t/; $yt{NFC($p)} = $id if $id }
close $t;

open my $h, '<:utf8', $in or die "$in: $!";
my $html = do { local $/; <$h> };
close $h;

# src/href 값 → 촬영영상 폴더 아래 경로 (퍼센트 인코딩이든 그냥 한글이든)
sub key {
  my $u = shift;
  my $b = encode_utf8($u);
  $b =~ s/%([0-9A-Fa-f]{2})/chr hex $1/ge;
  my $s = NFC(decode_utf8($b));
  $s =~ s/^.*?\Q$dir\E// or die "촬영영상 폴더 밖: $s\n";
  return $s;
}

my ($nv, $nt, $nl) = (0, 0, 0);
$html =~ s{<video class="lecvid"[^>]*?\ssrc="([^"]+)"[^>]*>\s*</video>}{
  my $k = key($1);
  if (my $id = $yt{$k}) {
    $nv++;
    qq{<iframe class="lecyt" data-src="https://www.youtube.com/embed/$id?rel=0&amp;enablejsapi=1" }
    . qq{allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>};
  } elsif ($k =~ /^2-3 .*TAKE[23]_/) {
    $nt++;
    qq{<div class="lecyt-todo">이 영상은 추후 올릴 예정입니다.</div>};
  } else { die "유튜브 짝 없음: $k\n" }
}ge;

$html =~ s{href="([^"]+\.mp4)"}{
  my $k = key($1);
  my $id = $yt{$k} or die "유튜브 짝 없음: $k\n";
  $nl++;
  qq{href="https://youtu.be/$id"};
}ge;

my $np = ($html =~ s{<iframe class="lecpdf"[^>]*>\s*</iframe>\s*<p><a href="[^"]+\.pdf"[^>]*>[^<]*</a></p>}
                    {<p class="lecyt-note">작업물 예시(PDF)는 강의에서만 보여 드립니다.</p>}g);

my @left = $html =~ /(?:src|href|data-src)="(\.\.\/[^"]*)"/g;
die "저장소 밖을 가리키는 것이 남았다:\n" . join("\n", @left) . "\n" if @left;

my $extra = <<'END';
<style>
.reveal section iframe.lecyt { display: block; margin: 0 auto; width: 924px; max-width: 100%; height: 520px; border: 0; }
.reveal .lecyt-todo { display: flex; align-items: center; justify-content: center; margin: 0 auto; width: 924px; max-width: 100%; height: 520px; border: 1px dashed #bbb; border-radius: 8px; color: #888; font-size: 23px; }
.reveal .slides section .lecyt-note { text-align: center; margin-top: 200px; color: #888; }
</style>
<script>
// 탭을 바꾸면 그 탭셋 안의 유튜브는 멈춘다 (강의용 video-keys.html 의 «탭 바꾸면 멈춤» 과 같게)
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.panel-tabset').forEach(function(ts) {
    ts.addEventListener('click', function(e) {
      if (!e.target.closest('.panel-tabset-tabby a, [role="tab"]')) return;
      ts.querySelectorAll('iframe.lecyt').forEach(function(f) {
        if (f.contentWindow) f.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
      });
    });
  });
});
</script>
END
$html =~ s{</body>}{$extra</body>} or die "</body> 없음\n";

open my $o, '>:utf8', $out or die "$out: $!";
print $o $html;
close $o;
print "$out — 유튜브 $nv · 추후 업로드 $nt · 링크 $nl · PDF 뺌 $np\n";

# 첫 주소(…/ssu-261026-/)는 게시용으로 — quarto 가 만드는 index.html 은 강의용을 가리키므로 덮어쓴다
open my $ix, '>:utf8', 'docs/index.html' or die "docs/index.html: $!";
print $ix qq{<!doctype html>\n<html><head><meta charset="utf-8"><title>강의노트</title>\n<meta http-equiv="refresh" content="0;URL='261026-web.html'" /></head><body></body></html>\n};
close $ix;
