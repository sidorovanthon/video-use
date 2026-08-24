[CmdletBinding()]
param(
    [string]$ObsRoot = 'M:\videos\OBS',
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'

$prepRoot = Join-Path $ObsRoot 'prep'
$yearRoot = Join-Path $ObsRoot '2026'

function Get-FullPath([string]$Path) {
    [System.IO.Path]::GetFullPath($Path).TrimEnd('\')
}

function Get-LongPath([string]$Path) {
    $full = Get-FullPath $Path
    if ($full.StartsWith('\\')) {
        return '\\?\UNC\' + $full.Substring(2)
    }
    return '\\?\' + $full
}

function Test-LeafLong([string]$Path) {
    [System.IO.File]::Exists((Get-LongPath $Path))
}

function Test-DirectoryLong([string]$Path) {
    [System.IO.Directory]::Exists((Get-LongPath $Path))
}

function Assert-UnderRoot([string]$Path, [string]$Root) {
    $fullPath = Get-FullPath $Path
    $fullRoot = Get-FullPath $Root
    if (-not ($fullPath.Equals($fullRoot, [StringComparison]::OrdinalIgnoreCase) -or
        $fullPath.StartsWith($fullRoot + '\', [StringComparison]::OrdinalIgnoreCase))) {
        throw "Path escapes expected root: $fullPath (root: $fullRoot)"
    }
}

function Get-CanonicalStem([string]$Stem) {
    $variantFamilies = @(
        'Choosing a technology stack when writing a desktop application is no less important than when developing web applications',
        'The beauty of delegating tasks to AI',
        'The time has come when you no longer need to look for the proverbial computer master to fix your Windows'
    )
    foreach ($family in $variantFamilies) {
        if ($Stem -in @("$family (1)", "$family (2)")) {
            return $family
        }
    }
    return $Stem
}

function Get-StemFromPrepFolder([string]$Name) {
    if ($Name -notmatch '^\d{4}-\d{2}-\d{2} (.+)$') {
        throw "Unexpected prep video-folder name: $Name"
    }
    return $Matches[1]
}

function Get-DateFromPrepFolder([string]$Name) {
    if ($Name -notmatch '^(\d{4}-\d{2}-\d{2}) ') {
        throw "Unexpected prep video-folder name: $Name"
    }
    return $Matches[1]
}

if (-not (Test-Path -LiteralPath $prepRoot -PathType Container)) {
    throw "Prep root not found: $prepRoot"
}
if (-not (Test-Path -LiteralPath $yearRoot -PathType Container)) {
    throw "Year root not found: $yearRoot"
}

# This helper implements the legacy recording-date layout. Fail closed once
# the script-date convention is present; use reorganize_by_script_date.py for
# the current layout instead of mixing the two migration schemes.
$scriptDatedFolders = @(Get-ChildItem -LiteralPath $prepRoot -Directory | Where-Object {
    $_.Name -match '^\d{4}-\d{2}$'
} | ForEach-Object {
    Get-ChildItem -LiteralPath $_.FullName -Directory | Where-Object {
        $_.Name -match '\[REC \d{4}-\d{2}-\d{2}\]$'
    }
})
if ($scriptDatedFolders.Count -gt 0) {
    throw 'Script-date prep folders already exist. Use helpers/reorganize_by_script_date.py; the legacy organizer is disabled.'
}

$moves = [System.Collections.Generic.List[object]]::new()
$replacements = [System.Collections.Generic.List[object]]::new()
$targetsByStem = @{}
$existingFolderByStem = @{}

function Add-Replacement([string]$OldPath, [string]$NewPath) {
    $script:replacements.Add([pscustomobject]@{
        Old = Get-FullPath $OldPath
        New = Get-FullPath $NewPath
    })
}

function Add-Move([string]$Kind, [string]$Source, [string]$Destination) {
    Assert-UnderRoot $Source $ObsRoot
    Assert-UnderRoot $Destination $prepRoot
    $script:moves.Add([pscustomobject]@{
        Kind = $Kind
        Source = Get-FullPath $Source
        Destination = Get-FullPath $Destination
    })
    Add-Replacement $Source $Destination
}

# Existing video folders may be flat (before migration) or already under a month
# after a safely completed/partially completed pass. Service folders are excluded.
$flatPrepFolders = @(Get-ChildItem -LiteralPath $prepRoot -Directory | Where-Object {
    $_.Name -match '^\d{4}-\d{2}-\d{2} '
})
$monthlyPrepFolders = @(Get-ChildItem -LiteralPath $prepRoot -Directory | Where-Object {
    $_.Name -match '^\d{4}-\d{2}$'
} | ForEach-Object {
    Get-ChildItem -LiteralPath $_.FullName -Directory | Where-Object {
        $_.Name -match '^\d{4}-\d{2}-\d{2} '
    }
})
$existingPrepFolders = @($flatPrepFolders) + @($monthlyPrepFolders)

foreach ($folder in $existingPrepFolders) {
    $date = Get-DateFromPrepFolder $folder.Name
    $stem = Get-StemFromPrepFolder $folder.Name
    $month = $date.Substring(0, 7)
    $destination = Join-Path (Join-Path $prepRoot $month) $folder.Name
    $key = $stem.ToLowerInvariant()
    if ($targetsByStem.ContainsKey($key)) {
        throw "Duplicate existing prep stem: $stem"
    }
    $targetsByStem[$key] = $destination
    $existingFolderByStem[$key] = $folder.FullName
    if ($folder.Parent.FullName -eq $prepRoot) {
        Add-Move 'prep-folder' $folder.FullName $destination
    }
    else {
        # Preserve the path rewrite that a first pass would have recorded.
        Add-Replacement (Join-Path $prepRoot $folder.Name) $destination
    }

    # Reconstruct legacy source spellings for resumable EDL repair.
    Get-ChildItem -LiteralPath $folder.FullName -File -ErrorAction SilentlyContinue | Where-Object {
        $_.Extension.ToLowerInvariant() -in @('.mkv', '.mp4', '.mov')
    } | ForEach-Object {
        Add-Replacement (Join-Path $ObsRoot $_.Name) $_.FullName
        Add-Replacement (Join-Path (Join-Path $yearRoot $month) $_.Name) $_.FullName
    }
}

# Descriptive filenames are real video jobs. Timestamp-named OBS captures and
# Desktop 20* files are failed-take/service dumps and intentionally stay put.
$namedVideos = Get-ChildItem -LiteralPath $yearRoot -Recurse -File | Where-Object {
    $_.Extension.ToLowerInvariant() -in @('.mkv', '.mp4', '.mov') -and
    $_.BaseName -notmatch '^20\d\d-\d\d-\d\d \d\d-\d\d-\d\d' -and
    $_.BaseName -notmatch '^Desktop 20'
}

$videoGroups = $namedVideos | Group-Object { Get-CanonicalStem $_.BaseName }
foreach ($group in $videoGroups) {
    $stem = $group.Name
    $key = $stem.ToLowerInvariant()
    if ($targetsByStem.ContainsKey($key)) {
        $targetFolder = $targetsByStem[$key]
    }
    else {
        $date = ($group.Group | Sort-Object LastWriteTime | Select-Object -First 1).LastWriteTime.ToString('yyyy-MM-dd')
        $month = $date.Substring(0, 7)
        $folderName = "$date $stem"
        $targetFolder = Join-Path (Join-Path $prepRoot $month) $folderName
        $targetsByStem[$key] = $targetFolder
    }

    foreach ($file in $group.Group) {
        $destination = Join-Path $targetFolder $file.Name
        if ($existingFolderByStem.ContainsKey($key)) {
            $futureCollision = Join-Path $existingFolderByStem[$key] $file.Name
            if (Test-Path -LiteralPath $futureCollision) {
                throw "A prep folder already contains $($file.Name): $futureCollision"
            }
        }
        Add-Move 'source-video' $file.FullName $destination

        # edit-01..07 used the even older root-level source convention. Add that
        # historical spelling so EDL paths are repaired after the move.
        Add-Replacement (Join-Path $ObsRoot $file.Name) $destination
    }
}

$rootEditTargets = [ordered]@{
    'edit-01' = 'Desktop software licensing, it turns out, is also a whole story'
    'edit-02' = 'Who else is tired of endless monthly subscriptions and paid SaaS in the age of artificial intelligence'
    'edit-03' = 'The script for this video was written by a human being'
    'edit-04' = 'Curiously, it seems that in the world of web development, the pendulum has swung from builders and no-code solutions back toward code'
    'edit-05' = "every day I'm looking for tasks for myself that I'll be able to complete with the help of artificial intelligence"
    'edit-06' = 'The beauty of delegating tasks to AI'
    'edit-07' = "Here's what I've noticed about products used in work"
    'edit-08' = 'Any codebase has a README file for new contributors'
    'edit-09' = 'Working with AI agents very strongly reflects human behavior'
    'edit-10' = 'When an AI agent works with projects that lack a clear structure'
    'edit-11' = 'Tasks related to digging through the Bubble app export mess are still extremely resource-intensive'
    'edit-12' = 'How to Avoid Losing Context in a Complex Project When Working with AI'
    'edit-13' = 'How to Avoid Losing Context in a Complex Project When Working with AI Part 2'
    'edit-14' = 'How to Avoid Losing Context in a Complex Project When Working with AI Part 3'
    'edit-15' = 'How to Avoid Losing Context in a Complex Project When Working with AI Part 4'
}

foreach ($entry in $rootEditTargets.GetEnumerator()) {
    $editSource = Join-Path $ObsRoot $entry.Key
    if (-not (Test-DirectoryLong $editSource)) {
        throw "Expected legacy edit folder is missing: $editSource"
    }
    $key = $entry.Value.ToLowerInvariant()
    if (-not $targetsByStem.ContainsKey($key)) {
        throw "No target video folder found for $($entry.Key): $($entry.Value)"
    }
    $editDestination = Join-Path $targetsByStem[$key] $entry.Key
    Add-Move 'edit-folder' $editSource $editDestination
}

# Preflight: every source must exist, destinations must be unique, and no target
# may already exist. This also makes accidental re-runs fail closed.
$duplicateDestinations = $moves | Group-Object Destination | Where-Object Count -gt 1
if ($duplicateDestinations) {
    throw "Duplicate move destinations: $($duplicateDestinations.Name -join '; ')"
}
foreach ($move in $moves) {
    $sourceExists = if ($move.Kind -in @('prep-folder', 'edit-folder')) {
        Test-DirectoryLong $move.Source
    }
    else {
        Test-LeafLong $move.Source
    }
    if (-not $sourceExists) {
        throw "Move source does not exist: $($move.Source)"
    }
    if ((Test-DirectoryLong $move.Destination) -or (Test-LeafLong $move.Destination)) {
        throw "Move destination already exists: $($move.Destination)"
    }
}

$summary = [pscustomobject]@{
    VideoFolders = $targetsByStem.Count
    ExistingPrepFolders = $existingPrepFolders.Count
    NamedSourceFiles = $namedVideos.Count
    LegacyEditFolders = $rootEditTargets.Count
    TotalMoves = $moves.Count
    Mode = if ($Apply) { 'apply' } else { 'dry-run' }
}
$summary | Format-List
$moves | Group-Object Kind | Select-Object Name, Count | Format-Table -AutoSize

if (-not $Apply) {
    Write-Output 'Dry-run passed: no filesystem changes were made.'
    exit 0
}

$completedMoves = [System.Collections.Generic.List[object]]::new()
foreach ($move in $moves) {
    $parent = Split-Path -Parent $move.Destination
    if (-not (Test-DirectoryLong $parent)) {
        [System.IO.Directory]::CreateDirectory((Get-LongPath $parent)) | Out-Null
    }
    if ($move.Kind -in @('prep-folder', 'edit-folder')) {
        [System.IO.Directory]::Move((Get-LongPath $move.Source), (Get-LongPath $move.Destination))
    }
    else {
        [System.IO.File]::Move((Get-LongPath $move.Source), (Get-LongPath $move.Destination))
    }
    $completedMoves.Add($move)
}

# Repair operational absolute paths without rewriting historical prose. EDL JSON
# is the executable artifact used by render.py; replace slash, backslash, and
# JSON-escaped backslash spellings while preserving its original formatting.
$updatedEdls = [System.Collections.Generic.List[string]]::new()
$orderedReplacements = $replacements | Sort-Object { $_.Old.Length } -Descending
$edlFiles = Get-ChildItem -LiteralPath $prepRoot -Recurse -File -Filter 'edl*.json'
foreach ($edl in $edlFiles) {
    $text = [System.IO.File]::ReadAllText((Get-LongPath $edl.FullName))
    $updated = $text
    foreach ($replacement in $orderedReplacements) {
        $oldBack = $replacement.Old
        $newBack = $replacement.New
        $oldForward = $oldBack.Replace('\', '/')
        $newForward = $newBack.Replace('\', '/')
        $oldJsonBack = $oldBack.Replace('\', '\\')
        $newJsonBack = $newBack.Replace('\', '\\')
        $updated = $updated.Replace($oldJsonBack, $newJsonBack)
        $updated = $updated.Replace($oldForward, $newForward)
        $updated = $updated.Replace($oldBack, $newBack)
    }
    if ($updated -ne $text) {
        $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
        [System.IO.File]::WriteAllText((Get-LongPath $edl.FullName), $updated, $utf8NoBom)
        $updatedEdls.Add($edl.FullName)
    }
}

$brokenEdlSources = [System.Collections.Generic.List[object]]::new()
foreach ($edl in $edlFiles) {
    try {
        $data = [System.IO.File]::ReadAllText((Get-LongPath $edl.FullName)) | ConvertFrom-Json
        if ($null -eq $data.sources) { continue }
        foreach ($property in $data.sources.PSObject.Properties) {
            $sourceValue = [string]$property.Value
            if ([System.IO.Path]::IsPathRooted($sourceValue)) {
                $resolvedSource = $sourceValue
            }
            else {
                $resolvedSource = Join-Path $edl.DirectoryName $sourceValue
            }
            if (-not (Test-LeafLong $resolvedSource)) {
                $brokenEdlSources.Add([pscustomobject]@{
                    Edl = $edl.FullName
                    Key = $property.Name
                    Source = $sourceValue
                })
            }
        }
    }
    catch {
        $brokenEdlSources.Add([pscustomobject]@{
            Edl = $edl.FullName
            Key = '<parse-error>'
            Source = $_.Exception.Message
        })
    }
}

$logPath = Join-Path $prepRoot 'organization_log_2026-08-17.json'
$log = [ordered]@{
    timestamp = (Get-Date).ToString('o')
    summary = $summary
    moves = $completedMoves
    path_replacements = $orderedReplacements
    updated_edl_files = $updatedEdls
    broken_edl_sources = $brokenEdlSources
}
$log | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $logPath -Encoding utf8

if ($brokenEdlSources.Count -gt 0) {
    $brokenEdlSources | Format-Table -Wrap -AutoSize
    throw "Migration completed, but $($brokenEdlSources.Count) EDL source references are unresolved. See $logPath"
}

Write-Output "Migration completed successfully. Audit log: $logPath"
